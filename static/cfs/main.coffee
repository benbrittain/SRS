class @Card extends Backbone.Model
  url: =>
    string = "/cards"
    string += "/#{@id}"  unless @isNew()
    string

class @Deck extends Backbone.Collection
  model: Card
