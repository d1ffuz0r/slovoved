var Inline = Quill.import('blots/inline');
var Module = Quill.import('core/module');
var quill;
var wordsCache = {};
var alternativeContainer = $('.word-alternatives');


function cleanText(txt) {
  return txt.replace(/[^А-Яа-яA-Za-z\s\-]/g, '');
}

var calculateSlovovedScore = function(totalWords, altWords) {
  var percentage,
      label,
      emoji;

  if (!altWords) {
      percentage = 10;
  } else {
      percentage = 10 - Math.ceil((altWords / totalWords) * 10);
  }

  if (percentage == 10) {
      label = 'наш человек';
      emoji = '👍';
  } else if (0 < percentage && percentage <= 4) {
      label = 'вы наверняка английский шпион';
      emoji = '👎';
  } else if (4 < percentage && percentage < 10) {
      label = 'похоже, что вы американский партнёр';
      emoji = '✋';
  }

  return {
      label: label,
      score: percentage,
      emoji: emoji
  };
};

var activatePopups = function() {
    $('.sv-detected').hover(
        function(ev){
            var text = ev.target.innerText;
            var altWord = wordsCache[text]['replacement'];
            var altText = 'Слово <b>'+ text + '</b> может быть заменено на <b>' +  altWord + '</b>';
            $(ev.target).popover({html: true, content: altText}).popover('show');
        },
        function(ev){
            $(ev.target).popover('hide');
        }
    );
}

var processResponse = function(response) {
    alternativeContainer.html('');
    response['results'].forEach(function(word) {
        var originalWord = word['original'],
            alternativeWord = word['replacement'];

        wordsCache[originalWord] = word;

        alternativeContainer.append('<p>' + originalWord + ' <i class="fa fa-long-arrow-right"></i> ' + alternativeWord + '</p>')

        quill.formatText(word['position'], word['length'], 'badword', true, 'silent')
    });

    var slovovedScore = calculateSlovovedScore(response.total_count, response.bad_count);
    var infoLabel = slovovedScore.score + '/10 слововедов ' + slovovedScore.emoji;
    var infoText = 'Из ' + response.total_count + ' слов найдено ' + response.bad_count + ' заимстоваваний - ' + slovovedScore.label;

    $('.stats-info .word-title').text(infoLabel);
    $('.stats-info .word-info').text(infoText);

    activatePopups();
    $(".stats-info").show();
    $(".stats-example").hide();
}


var checkWords = function(text) {
    if (text == '' || text == '\n') {
        return
    }
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    data = {
        text: text
    }
    req = $.post({
        url: '/api/validate/',
        datatype: "json",
        data: JSON.stringify(data),
    });
    req.done(processResponse);
}


class SlovoBlot extends Inline {
  static create (value) {
      var node = super.create();
      node.setAttribute('class', 'sv-detected');
      node.setAttribute('data-placement', 'top');
      node.setAttribute('data-toggle', 'popover');
      node.setAttribute('data-container', 'body');
      return node;
  }
}
SlovoBlot.blotName = 'badword';
SlovoBlot.tagName = 'em';


var Slovoved = function(quill, options) {
    this.quill = quill;
    this.options = options;

    var self = this;
    var currentIndex = 0;

    quill.on(Quill.events.EDITOR_CHANGE, function(eventName, delta, oldDelta, source) {
        if (eventName == Quill.events.SELECTION_CHANGE) {
            if (delta) {
                var text = quill.getText();
                currentIndex = delta.index;
                var currentWord = getCurrentWord(text, currentIndex);
                quill.removeFormat(currentWord[1], currentWord[2]);
                checkWords(text);
            }
        }
    });
};

Quill.register(SlovoBlot);
Quill.register('modules/slovoved', Slovoved);


var getCurrentWord = function(text, index) {
    if (text == ' ' || text == '\n') {
        return ''
    }

    var runleft = true;
    var runright = true;
    var ileft = 1;
    var iright = 1;
    var word;
    for(var i = 0; i<= 20; i++) {
        var look_back = index - ileft;
        var look_forward = index + iright;

        word = text.substring(look_back, look_forward);
        wl = word.length;

        firstChar = word.substring(0, 1);
        lastChar = word.substring(wl - 1, wl);

        if (look_back > 0 && (firstChar != ' ') && (firstChar != '\n') && (firstChar != '')) {
            ileft += 1;
        } else {
            runleft = false;
        }

        if ((lastChar != ' ') && (lastChar != '\n') && (lastChar != '')) {
            iright += 1;
        } else {
            runright = false;
        }

        if (!(runleft && runright)) {
            return [
                word.trim(),
                index - ileft,
                index + iright
            ];
        }
    }
}

$("body").ready(function(){
    quill = new Quill('#snow-container', {
        placeholder: 'Попробуйте написать что-нибудь....',
        modules: {
            slovoved: {
                statsContainer: '.stats-info'
            }
        }
    });

    var slovovedCachedText = localStorage.getItem('slovovedText')
    if (slovovedCachedText) {
        quill.setContents({'ops': [{insert: slovovedCachedText}]}, 'user');
            localStorage.removeItem('slovovedText')
    }

    $('.example-inert').click(function(){
        quill.setContents({ops: [{insert: 'Автоконцерны также предлагают сохранить возможность заключать консорциумы. Это должно помочь им окупить инвестиции в организацию выпуска новых ключевых узлов за счет разделения инвестиций между участниками консорциума.'}]}, 'user');
        checkWords(quill.getText());
    });
});
