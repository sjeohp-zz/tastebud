class BudsController < ApplicationController

  def show
    @bud = params[:bud_key]
  	@budstring = current_user.tags.to_a.map{|tag|tag.title}.join(', ')
	end
end
