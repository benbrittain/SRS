// Generated by CoffeeScript 1.3.3
(function() {
  var JST,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  JST = {};

  JST['decks'] = thermos.template(function(locals) {
    this.h2("Your decks");
    return this.ul('.bland', function() {
      var _this = this;
      locals.decks.each(function(deck) {
        return _this.li(function() {
          this.div(".view_deck.button", "" + (deck.get('name')) + " (" + deck.cards.length + " cards)", {
            "data-id": deck.id
          });
          return this.div(".edit_deck.button", {
            "data-id": deck.id
          }, "Edit");
        });
      });
      return this.li(function() {
        this.input('.new_deck_input', {
          type: 'text'
        });
        return this.div('.new_deck.button', "+ Add new deck");
      });
    });
  });

  JST['deck'] = thermos.template(function(locals) {
    this.h2(function() {
      this.span('.faux_link.go_back', 'Your decks');
      return this.text(" &raquo; " + (locals.deck.get('name')));
    });
    return this.div(function() {
      return JST['card']({
        card: locals.deck.cards.at(locals.index)
      });
    });
  });

  JST['card'] = thermos.template(function(locals) {
    this.div('.card', function() {
      return locals.card.get('front');
    });
    return this.div('.buttons', function() {
      this.div('.one.button', function() {
        return "1";
      });
      this.div('.two.button', function() {
        return "2";
      });
      this.div('.three.button', function() {
        return "3";
      });
      return this.div('.four.button', function() {
        return "4";
      });
    });
  });

  JST['edit_deck'] = thermos.template(function(locals) {
    var _this = this;
    this.h2(function() {
      this.span('.faux_link.go_back', 'Your decks');
      return this.text(" &raquo; Edit " + (locals.deck.get('name')));
    });
    this.div(function() {
      return JST['edit_card']();
    });
    this.div('.add_card.button', function() {
      return "+ Save card";
    });
    return locals.deck.cards.each(function(card) {
      return _this.div(function() {
        return JST['edit_card']({
          card: card
        });
      });
    });
  });

  JST['edit_card'] = thermos.template(function(locals) {
    var card;
    card = locals.card;
    return this.div('.card.clearfix', function() {
      this.textarea('.left', {
        placeholder: "What is the capital of France?"
      }, function() {
        if (card != null) {
          return card.get('front');
        }
      });
      return this.textarea('.right', {
        placeholder: "Paris"
      }, function() {
        if (card != null) {
          return card.get('back');
        }
      });
    });
  });

  this.Card = (function(_super) {

    __extends(Card, _super);

    function Card() {
      return Card.__super__.constructor.apply(this, arguments);
    }

    Card.prototype.urlRoot = "/cards";

    return Card;

  })(Backbone.Model);

  this.Deck = (function(_super) {

    __extends(Deck, _super);

    function Deck() {
      this.initialize = __bind(this.initialize, this);
      return Deck.__super__.constructor.apply(this, arguments);
    }

    Deck.prototype.urlRoot = "/decks";

    Deck.prototype.initialize = function(attributes) {
      return this.cards = new Cards(attributes.cards);
    };

    return Deck;

  })(Backbone.Model);

  this.User = (function(_super) {

    __extends(User, _super);

    function User() {
      this.initialize = __bind(this.initialize, this);
      return User.__super__.constructor.apply(this, arguments);
    }

    User.prototype.initialize = function(attributes) {
      return this.decks = new Decks(attributes.decks);
    };

    return User;

  })(Backbone.Model);

  this.Cards = (function(_super) {

    __extends(Cards, _super);

    function Cards() {
      return Cards.__super__.constructor.apply(this, arguments);
    }

    Cards.prototype.model = Card;

    Cards.prototype.url = '/decks';

    return Cards;

  })(Backbone.Collection);

  this.Decks = (function(_super) {

    __extends(Decks, _super);

    function Decks() {
      return Decks.__super__.constructor.apply(this, arguments);
    }

    Decks.prototype.model = Deck;

    Decks.prototype.url = '/decks';

    return Decks;

  })(Backbone.Collection);

  this.DecksView = (function(_super) {

    __extends(DecksView, _super);

    function DecksView() {
      this.editDeck = __bind(this.editDeck, this);

      this._createDeckError = __bind(this._createDeckError, this);

      this._createDeckSuccess = __bind(this._createDeckSuccess, this);

      this.createDeck = __bind(this.createDeck, this);

      this.inputDeck = __bind(this.inputDeck, this);

      this.viewDeck = __bind(this.viewDeck, this);

      this.remove = __bind(this.remove, this);

      this.render = __bind(this.render, this);

      this.initialize = __bind(this.initialize, this);
      return DecksView.__super__.constructor.apply(this, arguments);
    }

    DecksView.prototype.template = JST['decks'];

    DecksView.prototype.events = {
      'click .view_deck': 'viewDeck',
      'click .new_deck': 'createDeck',
      'keydown .new_deck_input': 'inputDeck',
      'click .edit_deck': 'editDeck'
    };

    DecksView.prototype.initialize = function() {
      return this.collection.on('add remove', this.render);
    };

    DecksView.prototype.render = function() {
      this.$el.html(this.template({
        decks: this.collection
      }));
      return this;
    };

    DecksView.prototype.remove = function() {
      this.collection.off('add remove', this.render);
      return DecksView.__super__.remove.call(this);
    };

    DecksView.prototype.viewDeck = function(e) {
      var $deck, $div, deck, deckView;
      $div = $("<div/>");
      $div.insertAfter(this.$el);
      this.$el.hide();
      $deck = this.$el.find(e.target);
      if (!$deck.hasClass('view_deck')) {
        $deck = $deck.closest('.view_deck');
      }
      deck = this.collection.get($deck.data('id'));
      deckView = new DeckView({
        model: deck,
        el: $div,
        parent: this
      });
      return deckView.render();
    };

    DecksView.prototype.inputDeck = function(e) {
      if (e.which === 13) {
        return this.createDeck();
      }
    };

    DecksView.prototype.createDeck = function() {
      var deck, name, token;
      token = $("meta[name='username']").attr("content");
      name = this.$el.find('.new_deck_input').val();
      deck = new Deck({
        name: name,
        username: token
      });
      return deck.save(null, {
        success: this._createDeckSuccess,
        error: this._createDeckError
      });
    };

    DecksView.prototype._createDeckSuccess = function(deck) {
      return this.collection.add(deck);
    };

    DecksView.prototype._createDeckError = function() {};

    DecksView.prototype.editDeck = function(e) {
      var $deck, deck;
      $deck = this.$el.find(e.target);
      if (!$deck.hasClass('edit_deck')) {
        $deck = $deck.closest('.edit_deck');
      }
      deck = this.collection.get($deck.data('id'));
      return this.$el.html(JST['edit_deck']({
        deck: deck
      }));
    };

    return DecksView;

  })(Backbone.View);

  this.DeckView = (function(_super) {

    __extends(DeckView, _super);

    function DeckView() {
      this.goBack = __bind(this.goBack, this);

      this.render = __bind(this.render, this);

      this.initialize = __bind(this.initialize, this);
      return DeckView.__super__.constructor.apply(this, arguments);
    }

    DeckView.prototype.template = JST['deck'];

    DeckView.prototype.events = {
      'click .go_back': 'goBack'
    };

    DeckView.prototype.initialize = function(options) {
      this.parent = options.parent;
      return this.index = 0;
    };

    DeckView.prototype.render = function() {
      this.$el.html(this.template({
        deck: this.model,
        index: this.index
      }));
      return this;
    };

    DeckView.prototype.goBack = function() {
      this.remove();
      return this.parent.$el.show();
    };

    return DeckView;

  })(Backbone.View);

  this.DeckView = (function(_super) {

    __extends(DeckView, _super);

    function DeckView() {
      this.goBack = __bind(this.goBack, this);

      this.render = __bind(this.render, this);

      this.initialize = __bind(this.initialize, this);
      return DeckView.__super__.constructor.apply(this, arguments);
    }

    DeckView.prototype.template = JST['edit_deck'];

    DeckView.prototype.events = {
      'click .go_back': 'goBack'
    };

    DeckView.prototype.initialize = function(options) {
      this.parent = options.parent;
      return this.index = 0;
    };

    DeckView.prototype.render = function() {
      this.$el.html(this.template({
        deck: this.model,
        index: this.index
      }));
      return this;
    };

    DeckView.prototype.goBack = function() {
      this.remove();
      return this.parent.$el.show();
    };

    return DeckView;

  })(Backbone.View);

}).call(this);
