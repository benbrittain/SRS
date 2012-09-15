JST = {}
JST['decks'] = thermos.template (locals) ->
  @h2 "Your decks"
  @ul '.bland', ->
    locals.decks.each (deck) =>
      @li ".view_deck.button", "#{deck.get('name')} (#{deck.cards.length} cards)", "data-id": deck.id
    @li ->
      @input '.new_deck_input', type: 'text'
      @div '.new_deck.button', "+ Add new deck"
JST['deck'] = thermos.template (locals) ->
  @h2 ->
    @span '.faux_link.go_back', 'Your decks'
    @text " &raquo; #{locals.deck.get('name')}"
  # TODO: Display cards
JST['card'] = thermos.template ->
  @div

# Models
class @Card extends Backbone.Model
  urlRoot: "/cards"

class @Deck extends Backbone.Model
  urlRoot: "/decks"
  initialize: (attributes) =>
    @cards = new Cards(attributes.cards)

class @User extends Backbone.Model
  initialize: (attributes) =>
    @decks = new Decks(attributes.decks)

# Collections
class @Cards extends Backbone.Collection
  model: Card
  url: '/decks'

class @Decks extends Backbone.Collection
  model: Deck
  url: '/decks'

# Views
class @DecksView extends Backbone.View
  template: JST['decks']

  events:
    'click .view_deck': 'viewDeck'
    'click .new_deck': 'createDeck'
    'keydown .new_deck_input': 'inputDeck'

  initialize: =>
    @collection.on 'add remove', @render

  render: =>
    @$el.html @template(decks: @collection)
    this

  remove: =>
    @collection.off 'add remove', @render
    super()

  viewDeck: (e) =>
    $div = $("<div/>")
    $div.insertAfter @$el
    @$el.hide()
    $deck = @$el.find(e.target)
    $deck = $deck.closest('.view_deck')  unless $deck.hasClass('view_deck')
    deck = @collection.get($deck.data('id'))
    deckView = new DeckView(model: deck, el: $div, parent: this)
    deckView.render()

  inputDeck: (e) =>
    @createDeck()  if e.which == 13

  createDeck: =>
    token = $("meta[name='username']").attr("content")
    name = @$el.find('.new_deck_input').val()
    deck = new Deck(name: name, username: token)
    deck.save(null, success: @_createDeckSuccess, error: @_createDeckError)

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
    @parent.$el.show()
