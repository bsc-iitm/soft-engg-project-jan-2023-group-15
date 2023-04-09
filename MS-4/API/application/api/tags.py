from flask_restful import marshal, reqparse
from application.helpers import token_required, BaseAPIClass, CustomException, get_user
from application.database import db
from application.models.user import User
from application.models.tickets import Tags, SupportStaffTags
from application.response_fields import tag_output_with_response_fields

tag_req = reqparse.RequestParser()
tag_req.add_argument("tag_title", required=False, type=str, trim=True, help='Title is required', store_missing="")

edit_tag_req = reqparse.RequestParser()
edit_tag_req.add_argument("tag_id", required=True, type=str, trim=True, help='Tag is required')
edit_tag_req.add_argument("tag_title", required=False, type=str, trim=True, help='Title is required', store_missing="")

delete_tag_req = reqparse.RequestParser()
delete_tag_req.add_argument("tag_id", required=True, type=str, trim=True, help='Tag is required')

support_tag = reqparse.RequestParser()
support_tag.add_argument("tag_id", required=True, type=str, trim=True, help='Tag is required')
support_tag.add_argument("user_id", required=True, type=str, trim=True, help='User is required')

def _get_tag(tag_id):
    tag = db.session.query(Tags).filter(Tags.id == tag_id, Tags.status == Tags.STATUS.ACTIVE).first()
    if tag == None:
        raise CustomException(("Tag does not exist", 404))
    return tag

class TagManagement(BaseAPIClass):

    
    
    @token_required("GET")
    def get(self, key):
        try:
            tag = db.session.query(Tags).filter(Tags.status == Tags.STATUS.ACTIVE).all()
            self.data = marshal(tag, tag_output_with_response_fields)
        except CustomException as e:
            self.custom_code = 3001
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 3002
            self._exception_occured(e, False)

        return self._get_response()
    
    @token_required()
    def post(self, key):
        try:
            args = tag_req.parse_args()
            tag_title = args.get('tag_title', "")

            if len(tag_title) == 0:
                raise CustomException("Title is empty")
            
            tag_title = str(tag_title).lower()
            print(tag_title)
            admin = get_user(key, admin=True)
            print(admin)

            already_exist = db.session.query(Tags).filter(Tags.tag_title == tag_title).first()

            if already_exist:
                if already_exist.status == Tags.STATUS.DELETED:
                    already_exist.status = Tags.STATUS.ACTIVE
                    db.session.add(already_exist)
                    db.session.commit()
                    self.message = "Tag with same name is restored"
                    self.data = marshal(already_exist, tag_output_with_response_fields)
                else:
                    raise CustomException("Tag with same title already exists")
            else:
                tag = Tags(
                    tag_title=tag_title,
                    created_by_id=admin.id
                )

                db.session.add(tag)
                db.session.commit()

                self.data = marshal(tag, tag_output_with_response_fields)
                self.message = "Tag is created successfully!!!"

        except CustomException as e:
            self.custom_code = 3003
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 3004
            self._exception_occured(e, False)

        return self._get_response()
    
    @token_required()
    def put(self, key):
        try:
            args = edit_tag_req.parse_args()
            tag_id = args.get('tag_id', "")
            tag_title = args.get('tag_title', "")

            if len(tag_title) == 0:
                raise CustomException("Title is empty")
            
            admin = get_user(key, admin=True)
            
            tag = _get_tag(tag_id)

            if tag.created_by_id != admin.id:
                raise CustomException(("Forbidden to update this tag", 403))
            
            tag_title = str(tag_title).lower()

            if tag_title == tag.tag_title:
                raise CustomException("New title is same old title")
            
            already_exist = db.session.query(Tags).filter(Tags.tag_title == tag_title).first()

            if already_exist:
                if already_exist.status == Tags.STATUS.DELETED:
                    raise CustomException("Tag with name is in inactive state, Please create a new tag or change the title of this tag")
                else:
                    raise CustomException("Tag with same title already exists")
                
            
            tag.tag_title = tag_title
            db.session.add(tag)
            db.session.commit()

            self.data = marshal(tag, tag_output_with_response_fields)
            self.message = "Successfully updated the tag"

        except CustomException as e:
            self.custom_code = 3005
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 3006
            self._exception_occured(e, False)

        return self._get_response()

    @token_required()
    def delete(self, key):
        try:
            args = delete_tag_req.parse_args()
            tag_id = args.get('tag_id', "")

            admin = get_user(key, admin=True)
            
            tag = _get_tag(tag_id)

            if tag.created_by_id != admin.id:
                raise CustomException(("Forbidden to delete this tag", 403))
            
            tag.status = Tags.STATUS.DELETED
            db.session.add(tag)
            db.session.commit()

            self.data = {}
            self.message = "Tag status is changed to inactive"

        except CustomException as e:
            self.custom_code = 3007
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 3008
            self._exception_occured(e, False)

        return self._get_response()

class SupportStaffTagManagement(BaseAPIClass):
        
    @token_required()
    def post(self, key):
        try:
            args = support_tag.parse_args()
            user_id = args.get('user_id', "")
            tag_id = args.get("tag_id", "")

            admin = get_user(key, admin=True)
            user = get_user(user_id)

            if user.role != User.Role.SUPPORT_STAFF:
                raise CustomException("User is not support staff")
            
            tag = _get_tag(tag_id)

            staff_tag = db.session.query(SupportStaffTags).filter(
                SupportStaffTags.user_id == user.id,
                SupportStaffTags.tag_id == tag.id,
            ).first()

            if staff_tag:
                if staff_tag.status == SupportStaffTags.STATUS.ACTIVE:
                    raise CustomException("tag is already assigned to user")
                else:
                    staff_tag.status = SupportStaffTags.STATUS.ACTIVE
            else:
                staff_tag = SupportStaffTags(
                    user_id = user.id,
                    tag_id = tag.id,
                    created_by_id = admin.id
                )

            db.session.add(staff_tag)
            db.session.commit()
            self.message = "Successfully assigned tag to support staff"
        except CustomException as e:
            self.custom_code = 3009
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 3010
            self._exception_occured(e, False)

        return self._get_response()
    
    @token_required()
    def delete(self, key):
        try:
            args = support_tag.parse_args()
            user_id = args.get('user_id', "")
            tag_id = args.get("tag_id", "")

            admin = get_user(key, admin=True)
            user = get_user(user_id)

            if user.role != User.Role.SUPPORT_STAFF:
                raise CustomException("User is not support staff")
            
            tag = _get_tag(tag_id)
            
            staff_tag = db.session.query(SupportStaffTags).filter(
                SupportStaffTags.user_id == user.id,
                SupportStaffTags.tag_id == tag.id,
                SupportStaffTags.status == SupportStaffTags.STATUS.ACTIVE,
            ).first()

            if staff_tag == None:
                raise CustomException("Tag is not assigned to user")
            
            staff_tag.status = SupportStaffTags.STATUS.DELETED
            db.session.add(staff_tag)
            db.session.commit()
            self.message = "Successfully removed tag from support staff"
        except CustomException as e:
            self.custom_code = 3011
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 3012
            self._exception_occured(e, False)

        return self._get_response()
    