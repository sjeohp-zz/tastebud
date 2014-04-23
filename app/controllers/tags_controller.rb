class TagsController < ApplicationController
  
  def create
    tag = Tag.find_or_create_by(tag_params)
    user = current_user
    user.tags.delete_if { |ut| ut.key == tag.key }
    user.tags << tag
    redirect_to '/profile'
  end
  
  private
  
  def tag_params
    params.require(:tag).permit(:title)
  end
end
