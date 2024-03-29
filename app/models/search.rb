class Search
  include Mongoid::Document
  include Mongoid::Timestamps

  field :term, type: String
  field :key, type: String
  field :results, type: Array, default: []
end
