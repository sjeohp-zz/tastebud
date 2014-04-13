class SearchController < ApplicationController
  
  def create
    term = search_params
    tag = Tag.where(key: term[:key]).first
    return get_similar(term) if !tag
    hash = {}
    p tag.users.to_a
    tag.users.each do |u|
      u.tags.each do |t|
        if hash.key?(t.key)
          hash[t.key] += 1
        else
          hash[t.key] = 1
        end
      end
    end
    @search.results = hash.sort_by{|k, v| v}
  end
  
  def search_results
    @search.results
  end
  
  def search_params
    params.require(:search).permit(:key, :medium)
  end
  
  private
  
  def get_similar(term)
    
  end
  
end
