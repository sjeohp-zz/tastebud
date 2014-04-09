class UsersController < ApplicationController
  
  def new
    @user = User.new
  end
  
  def create
    p user_params
    @user = User.new(user_params)
    if @user.save
      redirect_to sign_in, :notice => "Successfully signed up."
    else
      render "sign_up"
    end
  end
  
  private

  def user_params
    params.require(:user).permit(:email, :password, :password_confirmation)
  end
  
end
