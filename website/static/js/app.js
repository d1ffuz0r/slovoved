var Inline = Quill.import('blots/inline');
var Module = Quill.import('core/module');
var slovoTimer;
var wordsCache = {};

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

//function cleanText(txt) {
//  return txt.replace(/[^А-Яа-яA-Za-z\s\-]/g, '');
//}

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


var processWords = function() {
//  var index = 0;
  var words = quill.getText();
  console.log(words);

  $.ajaxSetup({
      headers: { 'X-CSRFToken': csrftoken }
  });

  req = $.post({
    url: '/api/validate/',
    datatype: "json",
    data: {text: words},
  });
  req.done(function(response) {
    console.log(response)
  });

//  var alternativeContainer = $('.word-alternatives');
//  alternativeContainer.html('');
//
//  for (var word of words) {
//    var wordLength = word.length;
//    word = cleanText(word);
//
//    var alternative = findAlternative(word);
//    if (alternative) {
//      wordsCache[word] = alternative;
//      quill.formatText(index, index + wordLength, 'badword', true, 'silent');
//      alternativeContainer.append('<p>' + word + ' <i class="fa fa-long-arrow-right"></i> ' + alternative[1] + '</p>')
//    } else {
//      quill.removeFormat(index - 1, index + wordLength, 'badword', true, 'silent');
//    }
//    index += wordLength + 1;
//  }
//
//  $(".stats-example").hide();
//  $(".stats-info").show();
//  $('.sv-detected').hover(
//    function(ev){
//      var text = cleanText(ev.target.innerText);
//      var altWord = wordsCache[text];
//      console.log(altWord)
//      var altText = 'Слово <b>'+ text + '</b> может быть заменено на <b>' +  altWord[1] + '</b>';
//      $(ev.target).popover({html: true, content: altText}).popover('show');
//    },
//    function(ev){
//      $(ev.target).popover('hide');
//    }
//  );
};

var Slovoved = function(quill, options) {
  this.quill = quill;
  this.options = options;

  var self = this;

  quill.on(Quill.events.EDITOR_CHANGE, function(eventName, delta, oldDelta, source) {
//    var slovovedScore = self.calculate();

//    var infoLabel = slovovedScore.score + '/10 слововедов ' + slovovedScore.emoji;
//    var infoText = 'Из '+slovovedScore.wordsCount+' слов найдено '+slovovedScore.altCount+' заимстоваваний - ' + slovovedScore.label;
//
//    $(options.statsContainer + ' .word-title').text(infoLabel);
//    $(options.statsContainer + ' .word-info').text(infoText);
//
    if (eventName == Quill.events.TEXT_CHANGE && source == 'user') {
      clearTimeout(slovoTimer);
      slovoTimer = setTimeout(processWords, 1000);
    }
  });
};

Slovoved.prototype.calculate = function() {
  var words = quill.getText();
  console.log(words);
//  var wordsCount = words.length;
//  var altCount = 0;
//
//  var counter = {};
//  for (var word of words) {
//      word = cleanText(word);
//      var alternative = findAlternative(word);
//
//      if (alternative) {
//          if (counter[alternative[0]]) {
//              counter[alternative[0]].counter += 1
//              altCount += 1;
//          } else {
//              counter[alternative[0]] = {
//                  counter: 1,
//                  alternative: alternative[1]
//              };
//              altCount += 1;
//          }
//      }
//  }
//
//  var slovovedScore = calculateSlovovedScore(wordsCount, altCount);
//
//  return {
//      wordsCount: wordsCount,
//      altCount: altCount,
//      label: slovovedScore.label,
//      score: slovovedScore.score,
//      emoji: slovovedScore.emoji,
//  };
};

Quill.register(SlovoBlot);
Quill.register('modules/slovoved', Slovoved);

var quill;

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
    quill.setContents({ops: [{insert: 'я у мамы дилер!'}]}, 'user');
  });
});