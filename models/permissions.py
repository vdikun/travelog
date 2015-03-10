""" permission logic for viewers and owners """

def can_upload_photo(user):
	return user.is_owner()
    
def can_view_photo(user, photo):
	if user.is_owner():
		return user.id == photo.o_id
	else:
		owner = get_owner(user)
		return owner.id == photo.o_id