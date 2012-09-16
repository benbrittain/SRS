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
        return _this.li('.clearfix', function() {
          this.a(".view_deck.button.left.round_left", "" + (deck.get('name')) + " (" + deck.cards.length + ")", {
            href: 'javascript:void(0);',
            "data-id": deck.id
          });
          return this.a(".edit_deck.button.small.left.round_right", {
            href: 'javascript:void(0);',
            "data-id": deck.id
          }, "Edit");
        });
      });
      return this.li('.clearfix', function() {
        this.input('.new_deck_input.round_left', {
          type: 'text',
          placeholder: 'Data Communications and Networks I'
        });
        return this.a('.new_deck.button.action.left.round_right', {
          href: 'javascript:void(0);'
        }, function() {
          return "Create deck";
        });
      });
    });
  });

  JST['deck'] = thermos.template(function(locals) {
    this.h2(function() {
      this.a('.go_back', {
        href: "javascript:void(0);"
      }, 'Your decks');
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
    return this.div('.buttons.clearfix', function() {
      this.div('.button.left.hr10', {
        "data-value": "1"
      }, function() {
        return "1";
      });
      this.div('.button.left.hr10', {
        "data-value": "2"
      }, function() {
        return "2";
      });
      this.div('.button.left.hr10', {
        "data-value": "3"
      }, function() {
        return "3";
      });
      return this.div('.button.left', {
        "data-value": "4"
      }, function() {
        return "4";
      });
    });
  });

  JST['edit_deck'] = thermos.template(function(locals) {
    var _this = this;
    this.h2(function() {
      this.a('.go_back', {
        href: "javascript:void(0);"
      }, 'Your decks');
      return this.text(" &raquo; Edit " + (locals.deck.get('name')));
    });
    this.div('.add_card_sides', function() {
      this.div('.clearfix', function() {
        this.div('.half_width.left.card_loc', 'Front');
        return this.div('.half_width.right.card_loc', 'Back');
      });
      return this.div(function() {
        return JST['edit_card']();
      });
    });
    this.a('.add_card.button.action.round_bottom.right', {
      href: 'javascript:void(0);'
    }, function() {
      return "Create card";
    });
    return locals.deck.cards.each(function(card) {
      return _this.div('.card.clearfix', function() {
        this.div('.left.round_left', function() {
          this.div('.card_loc', function() {
            return 'Front';
          });
          return this.p(function() {
            return card.get('front');
          });
        });
        return this.div('.right.round_right', function() {
          this.div('.card_loc', function() {
            return 'Back';
          });
          return this.p(function() {
            return card.get('back');
          });
        });
      });
    });
  });

  JST['edit_card'] = thermos.template(function(locals) {
    var card;
    card = locals.card;
    return this.div('.card.clearfix', function() {
      var klass;
      klass = "";
      if (card == null) {
        klass = ".small";
      }
      this.textarea(".left" + klass, {
        placeholder: "What is the capital of France?"
      }, function() {
        if (card != null) {
          return card.get('front');
        }
      });
      return this.textarea(".right" + klass, {
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
      this.cards = new Cards(attributes.cards);
      return this.cards.url = "" + (this.url()) + "/cards";
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
      this._createDeckError = __bind(this._createDeckError, this);

      this._createDeckSuccess = __bind(this._createDeckSuccess, this);

      this.createDeck = __bind(this.createDeck, this);

      this.inputDeck = __bind(this.inputDeck, this);

      this.editDeck = __bind(this.editDeck, this);

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
      return deckView.start();
    };

    DecksView.prototype.editDeck = function(e) {
      var $deck, $div, deck, deckView;
      $div = $("<div/>");
      $div.insertAfter(this.$el);
      this.$el.hide();
      $deck = this.$el.find(e.target);
      if (!$deck.hasClass('edit_deck')) {
        $deck = $deck.closest('.edit_deck');
      }
      deck = this.collection.get($deck.data('id'));
      deckView = new EditDeckView({
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
      var name, username;
      this.$('.new_deck_input').prop('disabled', true);
      username = $("meta[name='username']").attr("content");
      name = this.$('.new_deck_input').val();
      return this.collection.create({
        name: name,
        username: username
      }, {
        wait: true,
        success: this._createDeckSuccess,
        error: this._createDeckError
      });
    };

    DecksView.prototype._createDeckSuccess = function(deck) {
      return this.$('.new_deck_input').prop('disabled', false);
    };

    DecksView.prototype._createDeckError = function() {};

    return DecksView;

  })(Backbone.View);

  this.DeckView = (function(_super) {

    __extends(DeckView, _super);

    function DeckView() {
      this.displayNext = __bind(this.displayNext, this);

      this.sendScore = __bind(this.sendScore, this);

      this.goBack = __bind(this.goBack, this);

      this.render = __bind(this.render, this);

      this.start = __bind(this.start, this);

      this.initialize = __bind(this.initialize, this);
      return DeckView.__super__.constructor.apply(this, arguments);
    }

    DeckView.prototype.template = JST['deck'];

    DeckView.prototype.events = {
      'click .go_back': 'goBack',
      'click .buttons .button': 'sendScore'
    };

    DeckView.prototype.initialize = function(options) {
      this.parent = options.parent;
      return this.index = 0;
    };

    DeckView.prototype.start = function() {
      var username,
        _this = this;
      username = $("meta[name='username']").attr("content");
      return $.getJSON("" + (this.model.url()) + "/start", {
        username: username
      }, function(data) {
        return _this.displayNext(data.id);
      });
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

    DeckView.prototype.sendScore = function(e) {
      var score, username,
        _this = this;
      score = parseInt($(e.target).data('value'), 10);
      username = $("meta[name='username']").attr("content");
      return $.post("" + (this.model.url()) + "/score", {
        username: username,
        score: score
      }, function(data) {
        if (data.id != null) {
          return _this.displayNext(data.id);
        } else {
          return alert("Completed sequence. You're a winner.");
        }
      });
    };

    DeckView.prototype.displayNext = function(id) {
      var card;
      card = this.model.cards.get(id);
      this.index = this.model.cards.indexOf(card);
      return this.render();
    };

    return DeckView;

  })(Backbone.View);

  this.EditDeckView = (function(_super) {

    __extends(EditDeckView, _super);

    function EditDeckView() {
      this.deleteDeck = __bind(this.deleteDeck, this);

      this.createCard = __bind(this.createCard, this);

      this.remove = __bind(this.remove, this);

      this.goBack = __bind(this.goBack, this);

      this.render = __bind(this.render, this);

      this.initialize = __bind(this.initialize, this);
      return EditDeckView.__super__.constructor.apply(this, arguments);
    }

    EditDeckView.prototype.template = JST['edit_deck'];

    EditDeckView.prototype.events = {
      'click .go_back': 'goBack',
      'click .add_card': 'createCard',
      'click .delete_deck': 'deleteDeck'
    };

    EditDeckView.prototype.initialize = function(options) {
      return this.parent = options.parent, options;
    };

    EditDeckView.prototype.render = function() {
      this.$el.html(this.template({
        deck: this.model
      }));
      this.model.cards.on('add remove', this.render);
      return this;
    };

    EditDeckView.prototype.goBack = function() {
      this.remove();
      return this.parent.$el.show();
    };

    EditDeckView.prototype.remove = function() {
      this.model.cards.off('add remove', this.render);
      return EditDeckView.__super__.remove.call(this);
    };

    EditDeckView.prototype.createCard = function() {
      var back, front, username;
      front = this.$('.add_card_sides textarea.left').val();
      back = this.$('.add_card_sides textarea.right').val();
      username = $("meta[name='username']").attr("content");
      return this.model.cards.create({
        front: front,
        back: back,
        username: username
      });
    };

    EditDeckView.prototype.deleteDeck = function() {
      this.model.destroy();
      return this.goBack();
    };

    return EditDeckView;

  })(Backbone.View);

  $(function() {
    return $('input').first().focus();
  });

}).call(this);
