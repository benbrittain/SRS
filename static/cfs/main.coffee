JST = {}
JST['decks'] = thermos.template (locals) ->
  @h2 "Your decks"
  @ul '.bland', ->
    locals.decks.each (deck) =>
      @li ->
        @div ".view_deck.button", "#{deck.get('name')} (#{deck.cards.length} cards)", "data-id": deck.id
        @div ".edit_deck.button", "data-id": deck.id, "Edit"
    @li ->
      @input '.new_deck_input', type: 'text'
      @div '.new_deck.button', "+ Add new deck"
JST['deck'] = thermos.template (locals) ->
  @h2 ->
    @span '.faux_link.go_back', 'Your decks'
    @text " &raquo; #{locals.deck.get('name')}"
  @div ->
    JST['card'](card: locals.deck.cards.at(locals.index))

JST['card'] = thermos.template (locals) ->
  @div '.card', ->
    locals.card.get('front')
  @div '.buttons', ->
    @div '.one.button', -> "1"
    @div '.two.button', -> "2"
    @div '.three.button', -> "3"
    @div '.four.button', -> "4"

JST['edit_deck'] = thermos.template (locals) ->
  @h2 ->
    @span '.faux_link.go_back', 'Your decks'
    @text " &raquo; Edit #{locals.deck.get('name')}"
  @div '.add_card_sides', -> JST['edit_card']()
  @div '.add_card.button', -> "+ Save card"
  locals.deck.cards.each (card) =>
    @div -> JST['edit_card'](card: card)

JST['edit_card'] = thermos.template (locals) ->
  card = locals.card
  @div '.card.clearfix', ->
    @textarea '.left', placeholder: "What is the capital of France?", -> card.get('front')  if card?
    @textarea '.right', placeholder: "Paris", -> card.get('back')  if card?

# Models
class @Card extends Backbone.Model

class @Deck extends Backbone.Model
  urlRoot: "/decks"
  initialize: (attributes) =>
    @cards = new Cards(attributes.cards)
    @cards.url = "#{@url()}/cards"

class @User extends Backbone.Model
  initialize: (attributes) =>
    @decks = new Decks(attributes.decks)

# Collections
class @Cards extends Backbone.Collection
  model: Card

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
    'click .edit_deck': 'editDeck'

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

  editDeck: (e) =>
    $div = $("<div/>")
    $div.insertAfter @$el
    @$el.hide()
    $deck = @$el.find(e.target)
    $deck = $deck.closest('.edit_deck')  unless $deck.hasClass('edit_deck')
    deck = @collection.get($deck.data('id'))
    deckView = new EditDeckView(model: deck, el: $div, parent: this)
    deckView.render()

  inputDeck: (e) =>
    @createDeck()  if e.which == 13

  createDeck: =>
    # TODO: Don't do this.
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
    @index = 0

  render: =>
    @$el.html @template(deck: @model, index: @index)
    this

  goBack: =>
    @remove()
    @parent.$el.show()

class @EditDeckView extends Backbone.View
  template: JST['edit_deck']

  events:
    'click .go_back': 'goBack'
    'click .add_card': 'createCard'
    # TODO: Editing a card
    # TODO: Adding a card
    # TODO: Removing a card

  initialize: (options) =>
    {@parent} = options
    @index = 0

  render: =>
    @$el.html @template(deck: @model, index: @index)
    this

  goBack: =>
    @remove()
    @parent.$el.show()

  createCard: =>
    front = @$('.add_card_sides .left').val()
    back = @$('.add_card_sides .right').val()
    # TODO: Don't do this.
    username = $("meta[name='username']").attr("content")
    @model.cards.create({front, back, username})
