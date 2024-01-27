from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operations on Tags")


@blp.route("/store/<int:store_id>/tags")
class TagsInStore(MethodView):

    @jwt_required(fresh=False)
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()  # lazy="dynamic" means 'tags' is a query

    @jwt_required(fresh=False)
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(404, message="A tag with given name already exists in given store")
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(404, message=str(e))

        return tag

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsAndItems(MethodView):
    @jwt_required(fresh=False)
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store_id != tag.store_id:
            abort(
                500, message="Make sure item and tag belong to the same store before linking.")
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error in linking tag to item.")
        return tag

    @jwt_required(fresh=True)
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        if item.store_id != tag.store_id:
            abort(
                500, message="Make sure item and tag belong to the same store before linking.")
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error in unlinking tag to item.")
        return {"message": "Item removed from the tag", "item": item, "tag": tag}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @jwt_required(fresh=False)
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required(fresh=True)
    @blp.response(202, description="Deletes a tag it no item is tagged with it.",example={"message": "Tag deleted."},)
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(400, description="Returned if tag is assined to one or more items. in this case tag is not deleted.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(400, message="Could not delete tag. Make sure that tag is not associated with any items, then try again.")


@blp.route("/tags")
class AllTags(MethodView):
    @jwt_required(fresh=False)
    @blp.response(200, TagSchema(many=True))
    def get(self):
        return TagModel.query.all()