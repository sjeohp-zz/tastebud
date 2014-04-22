class UsersController < ApplicationController

  def new
    @user = User.new
  end
  
  def create
    @user = User.new(user_params)
    if @user.save
      session[:user_id] = @user.id
      redirect_to root_path, :notice => "Signed up!"
    else
      render "new"
    end
  end
  
  def show
    @tag = Tag.new
    @tagstring = current_user.tags.to_a.map{|tag|tag.key}.join(', ')
  end
  
  private
  
  def user_params
    params.require(:user).permit(:email, :password, :password_confirmation)
  end
  
end
