class Tag
  include Mongoid::Document
  include Mongoid::Timestamps
  
  has_and_belongs_to_many :users, validate: false, autosave: true
  has_and_belongs_to_many :ghosts, validate: false, autosave: true
  belongs_to :bud, inverse_of: :tags, validate: false, autosave: true
  
  field :title, type: String
  field :key, type: String
  field :count, type: Integer
  
  before_save :set_key
  before_save :set_bud
  before_save :update_count

  private

  def set_key
    self.key = key_from_string(self.title)
  end

  def set_bud
    self.bud = Bud.find_or_create_by(:key => self.key)
  end

  def update_count
    self.count = self.users.size + self.ghosts.size
  end

  def key_from_string(str)
    return (k = str.downcase.gsub(/[^0-9a-z]/, '')) == nil ? str : k
  end
end
