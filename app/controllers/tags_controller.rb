class TagsController < ApplicationController
  
  def create
    tag = Tag.find_or_create_by(tag_params)
    user = current_user
    if !user.tags.include?(tag)
      user.tags << tag
    end
    redirect_to '/profile'
  end
  
  private
  
  def tag_params
    params.require(:tag).permit(:key, :medium)
  end
  
end
