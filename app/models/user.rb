require 'bcrypt'

class User < ActiveRecord::Base
	include BCrypt

	attr_accessor :password, :password_confirmation

	validates :username, :email, :password, :presence => true
	validates :username, :uniqueness => true
	validates :username, length: { :minimum => 2 }
	validates :password, length: { :minimum => 6 }
	validates :password, :confirmation => true

	before_save :hash_password

	def hash_password
		self.password_hash = Password.create(@password)
	end

	def self.authenticate(username, password)
		user = User.find_by_username(username)
		return nil if user.nil?
		Password.new(user.password_hash) == password ? user : nil
	end
end
