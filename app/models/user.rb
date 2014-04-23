require 'bcrypt'
 
class User
  include Mongoid::Document
  include Mongoid::Timestamps
  include BCrypt
  
  has_and_belongs_to_many :tags, validate: false, autosave: true

  attr_accessor :password, :password_confirmation
  
  field :handle, type: String
  field :email, type: String
  field :password_hash, type: String
  
  validates_presence_of :handle, :message => "You need a handle."
  validates_uniqueness_of :handle, :message => "Someone else took that handle already."
  validates_presence_of :email, :message => "You must enter an email."
  validates_uniqueness_of :email, :message => "That email already in use."
  validates_length_of :password, :minimum => 6, :message => "Your password must have at least 6 characters."
  validates_confirmation_of :password, :message => "Password confirmation didn't match."
  
  before_save :downcase_email
  before_save :encrypt_password
  
  def self.find_by_email(email)
    u = User.where(email: email).first
  end
  
  def self.authenticate(email, password)
    user = self.find_by_email(email)
    return nil if user.nil?
    Password.new(user.password_hash) == password ? user : nil
  end
  
  def add_tag(tag)
    
  end

  protected
  
  def downcase_email
    self.email.downcase!
  end
  
  def encrypt_password
    self.password_hash = Password.create(@password)
  end
end