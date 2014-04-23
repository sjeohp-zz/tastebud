class ApplicationController < ActionController::Base
  helper :all # include all helpers, all the time
  protect_from_forgery # See ActionController::RequestForgeryProtection for details
 
  helper_method :current_user, :logged_in?
  # Scrub sensitive parameters from your log
  # filter_parameter_logging :password, :password_confirmation

  before_action :ghost_session
  before_action :new_search

  def ghost_session
    @ghost_session = Ghost.find_or_create_by(:session_id => request.session_options[:id], :remote_ip => request.remote_ip, :user => current_user)
  end

  def new_search
    @search = Search.new
  end
  
  def logged_in?
    session[:user_id].present?
  end
  
  def current_user
    return unless session[:user_id]
    @current_user ||= User.find(session[:user_id])
  end
  
  def require_user
    unless current_user
      store_location
      flash[:notice] = "You must be logged in to view this page"
      redirect_to new_session_url
      return false
    end
  end
  
  def store_location
    session[:return_to] = request.request_uri
  end
 
  def redirect_back_or_default(default)
    redirect_to(session[:return_to] || default)
    session[:return_to] = nil
  end
end