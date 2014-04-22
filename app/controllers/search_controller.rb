class SearchController < ApplicationController
  
  def create

    ghost = ghost_session

    term = search_params
    tag = Tag.where(key: term[:key]).first

    if !tag
      get_similar(term)
      tag = Tag.create(key: term[:key], medium: term[:medium])
      ghost.tags << tag if !ghost.tags.include?(tag)
      return
    end
    ghost.tags << tag if !ghost.tags.include?(tag)  

    hash = search_relation_tags(tag.ghosts, search_relation_tags(tag.users, {}))
    @search.results = hash.sort_by{|k, v| v}
  end

  def search_relation_tags(relation, hash)
    relation.each do |u|
      u.tags.each do |t|
        if hash.key?(t.key)
          hash[t.key] += 1
        else
          hash[t.key] = 1
        end
      end
    end
    return hash
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
