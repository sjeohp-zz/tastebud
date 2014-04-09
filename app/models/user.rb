# class User
#   include Mongoid::Document
#   
#   # field :username, type: String
#   field :email, type: String
#   field :password_hash, type: String
#   field :password_salt, type: String
#   
#   validates_presence_of :password
#   validates_confirmation_of :password
#   validates_presence_of :email
#   validates_uniqueness_of :email
#   
#   before_save :encrypt_password
#   
#   def encrypt_password
#     if password.present?
#       self.password_salt = BCrypt::Engine.generate_salt
#       self.password_hash = BCrypt::Engine.hash_secret(password, password_salt)
#     end
#   end
#   
#   def password=(arg)
#     @password = arg
#   end
#   
#   def password
#     @password
#   end
#   
# end


require 'bcrypt'

 
class User
  include Mongoid::Document
  include Mongoid::Timestamps
  include BCrypt
  include UsersHelper::ProtectedAttributes
 
  attr_protected :password_hash, :password_salt
  attr_accessor         :password, :password_confirmation
  # attr_protected        :password_hash
  
  field :email,         :type => String
  field :password_hash, :type => String
  field :accept_terms,  :type => Boolean
  
  validates_presence_of :email, :message => "Email Address is Required."
  validates_uniqueness_of :email, :message => "Email Address Already In Use. Have You Forgot Your Password?"
  # validates_format_of :email, :with => /^[-a-z0-9_+\.]+\@([-a-z0-9]+\.)+[a-z0-9]{2,4}$/i, :message => "Please Enter a Valid Email Address."
  validates_acceptance_of :accept_terms, :allow_nil => false, :accept => true, :message => "Terms and Conditions Must Be Accepted."
  validates_length_of :password, :minimum => 8, :message => "Password Must Be Longer Than 8 Characters."
  validates_confirmation_of :password, :message => "Password Confirmation Must Match Given Password."
  
  before_save :encrypt_password
  
  def self.find_by_email(email)
    first(conditions: { email: email })
  end
  
  def self.authenticate(email, password)
    if password_correct?(email, password)
      # Success!
      true
    else
      # Failed! :(
      false
    end
  end
  
  def self.password_correct?(user_email, password)
    user = find_by_email user_email
    return if user.nil?
    user_pass = Password.new(user.password_hash)
    user_pass == password
  end
  
  protected
  
  def encrypt_password
    self.password_hash = Password.create(@password)
  end
end