class PagesController < ApplicationController
  include UsersHelper
  
  def home
    @current_user = current_user
    if @current_user != nil
      
      
    else
      
      
    end
  end
end
