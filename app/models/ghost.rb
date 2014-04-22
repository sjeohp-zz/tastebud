class Ghost
  include Mongoid::Document

  has_and_belongs_to_many :tags, validate: false, autosave: true

  field :session_id, type: String
  field :remote_ip, type: String
  field :user_id, type: String
end
