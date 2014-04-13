class Tag
  include Mongoid::Document
  include Mongoid::Timestamps
  
  has_and_belongs_to_many :users, validate: false, autosave: true
  
  field :key, type: String
  field :medium, type: String
  
  before_save :downcase_fields
  
  def downcase_fields
    self.key.downcase!
    self.medium.downcase!
  end
end
