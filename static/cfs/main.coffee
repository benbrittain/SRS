JST = {}
JST['decks'] = thermos.template (locals) ->
  @h2 "Your decks"
  @ul '.bland', ->
    locals.decks.each (deck) =>
      @li '.clearfix', ->
        @a ".view_deck.button.left.round_left", "#{deck.get('name')} (#{deck.cards.length})", href: 'javascript:void(0);', "data-id": deck.id
        @a ".edit_deck.button.small.left.round_right", href: 'javascript:void(0);', "data-id": deck.id, "Edit"
    @li '.clearfix', ->
      @input '.new_deck_input.round_left', type: 'text', placeholder: 'Data Communications and Networks I'
      @a '.new_deck.button.action.left.round_right', href: 'javascript:void(0);', -> "Create deck"

JST['deck'] = thermos.template (locals) ->
  @h2 ->
    @a '.go_back', href: "javascript:void(0);", 'Your decks'
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
    @a '.go_back', href: "javascript:void(0);", 'Your decks'
    @text " &raquo; Edit #{locals.deck.get('name')}"
  @div '.add_card_sides', ->
    @div '.clearfix', ->
      @div '.half_width.left.card_loc', 'Front'
      @div '.half_width.right.card_loc', 'Back'
    @div -> JST['edit_card']()
  @a '.add_card.button.action.round_bottom.right', href: 'javascript:void(0);', -> "Create card"
  locals.deck.cards.each (card) =>
    @div '.card.clearfix', ->
      @div '.left.round_left', ->
        @div '.card_loc', -> 'Front'
        @p -> card.get('front')
      @div '.right.round_right', ->
        @div '.card_loc', -> 'Back'
        @p -> card.get('back')

JST['edit_card'] = thermos.template (locals) ->
  card = locals.card
  @div '.card.clearfix', ->
    klass = ""
    klass =  ".small"  unless card?
    @textarea ".left#{klass}", placeholder: "What is the capital of France?", -> card.get('front')  if card?
    @textarea ".right#{klass}", placeholder: "Paris", -> card.get('back')  if card?

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
    deckView.start()

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
    @$('.new_deck_input').prop('disabled', true)
    # TODO: Don't do this.
    username = $("meta[name='username']").attr("content")
    name = @$('.new_deck_input').val()
    @collection.create({name, username}, wait: true, success: @_createDeckSuccess, error: @_createDeckError)

  _createDeckSuccess: (deck) =>
    @$('.new_deck_input').prop('disabled', false)
    # TODO: Successful flash

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

  start: =>
    username = $("meta[name='username']").attr("content")
    $.post "#{@model.url()}/start", {username}, (data) =>
      card = @model.cards.get(data.id)
      @index = @model.cards.indexOf(card)
      @render()
    , 'json'

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
    'click .delete_deck': 'deleteDeck'
    # TODO: Editing a card
    # TODO: Adding a card
    # TODO: Removing a card

  initialize: (options) =>
    {@parent} = options

  render: =>
    @$el.html @template(deck: @model)
    @model.cards.on 'add remove', @render
    this

  goBack: =>
    @remove()
    @parent.$el.show()

  remove: =>
    @model.cards.off 'add remove', @render
    super()

  createCard: =>
    front = @$('.add_card_sides .left').val()
    back = @$('.add_card_sides .right').val()
    # TODO: Don't do this.
    username = $("meta[name='username']").attr("content")
    @model.cards.create({front, back, username})

  deleteDeck: =>
    @model.destroy()
    @goBack()

$ ->
  $('input').first().focus()
