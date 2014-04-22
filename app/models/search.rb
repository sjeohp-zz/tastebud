class Search
  include Mongoid::Document
  include Mongoid::Timestamps
  
  field :key, type: String
  field :medium, type: String
  field :results, type: Array, default: []
end
