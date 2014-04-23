class Bud
  include Mongoid::Document
  include Mongoid::Timestamps

  has_many :tags, inverse_of: :bud, validate: false, autosave: true

  field :key, type: String
end
