class SearchController < ApplicationController
  
  def create
    params = search_params
    term = params[:term]

    tag = Tag.find_or_create_by(:title => term)

    ghost = ghost_session
    ghost.tags.delete_if { |gt| gt.key == tag.key }
    ghost.tags << tag

    bud = Bud.where(:key => tag.key).first
    if !bud
      get_similar(term)
      bud = Bud.create(:key => tag.key)
      return
    end

    hash = search_t(bud, {})
    @search.results = hash.sort_by{ |k, v| v[:key_count] }
  end

  def search_t(bud, hash)
    bud.tags.each do |t| 
      hash = search_u(t, hash)
      hash = search_g(t, hash)
    end
    return hash
  end

  def search_u(tag, hash)
    tag.users.each { |u| hash = search_ut(u, hash) if u != current_user }
    return hash
  end

  def search_g(tag, hash)
    tag.ghosts.each { |g| hash = search_ut(g, hash) if (g != ghost_session) && g.user && (g.user != current_user) }
    return hash
  end

  def search_ut(u, hash)
    u.tags.each do |ut|
      if hash.key?(ut.key)
        hash[ut.key][:key_count] += 1
        if ut.count > hash[ut.key][:title_count]
          hash[ut.key][:title] = ut.title
          hash[ut.key][:title_count] = ut.count
        end
      else
        hash[ut.key] = { key_count: 1, title: ut.title, title_count: ut.count }
      end
    end
    return hash
  end
  
  def search_results
    @search.results
  end
  
  def search_params
    params.require(:search).permit(:term)
  end
  
  private
  
  def get_similar(term)
    
  end
end
