JST = {}
JST['decks'] = thermos.template (locals) ->
  @ul '.bland', ->
    locals.decks.each (deck) =>
      @li ".view_deck.button", "#{deck.get('name')}"
    @li '.new_deck', ->
      @input '.new_deck_input', type: 'text'
      @div '.button', "+ Add new deck"
JST['deck'] = thermos.template (locals) ->
  @span '.faux_link.go_back', '&laquo; Go back to list of decks'
  @h2 "#{locals.deck.get('name')}"
  # TODO: Display cards
JST['card'] = thermos.template ->
  @div

# Models
class @Card extends Backbone.Model
  urlRoot: "/cards"

class @Deck extends Backbone.Model
  urlRoot: "/decks"

class @User extends Backbone.Model
  initialize: (attributes) =>
    @decks = new Decks(attributes.decks)

# Collections
class @Decks extends Backbone.Collection
  model: Deck
  url: '/decks'

# Views
class @DecksView extends Backbone.View
  template: JST['decks']

  events:
    'click .view_deck': 'viewDeck'
    'click .new_deck': 'createDeck'

  initialize: =>
    @collection.on 'add remove', @render

  render: =>
    @$el.html @template(decks: @collection)
    this

  remove: =>
    @collection.off 'add remove', @render
    super()

  viewDeck: (e) =>
    @$el.hide()
    $div = $("<div/>")
    @$el.append($div)
    deckView = new DeckView(el: $div, parent: this)
    deckView.render()

  createDeck: =>
    token = $("meta[name='username']").attr("content")
    name = @$el.find('.new_deck_input').val()
    deck = new Deck(name: name, username: token)
    deck.save(success: @_createDeckSuccess, error: @_createDeckError)

  _createDeckSuccess: (deck) =>
    @collection.add(deck)

  _createDeckError: =>
    # TODO: Flash error

class @DeckView extends Backbone.View
  template: JST['deck']

  events:
    'click .go_back': 'goBack'
    # TODO: Editing a card
    # TODO: Adding a card
    # TODO: Removing a card

  initialize: (options) =>
    {@parent} = options

  render: =>
    @$el.html @template(deck: @model)
    this

  goBack: =>
    @remove()
    @parent.show()
