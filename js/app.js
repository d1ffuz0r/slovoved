var output_div = $(".words");
var stats_div = $(".stats");

function findAlternative(word) {
    var alternative = null;
    for (suggestion of words) {
        if (word.toLowerCase().trim().indexOf(suggestion[0]) !== -1) {
            return suggestion;
        };
    }
    return null;
}

function replaceWord(word, alternative) {
    return '<span style="color: red" title="' + word + ' -> ' + alternative + '"> '+ word + '</span>';
}

$("body").ready(function(){
    $("#check").click(function() {
        $("#resultdiv").show();

        var text = $("#text").val();
        if (text === '') {
            alert("введите текст");
            return
        }
        var output = [];

        var words = text.split(' ');

        var counter = {};

        for (word of words) {
            var alternative = findAlternative(word);
            var newWord = word;
            if (alternative) {
                if (counter[alternative[0]]) {
                    counter[alternative[0]] += 1
                } else {
                    counter[alternative[0]] = 1;
                }
                newWord = replaceWord(word, alternative[1]);
            }
            output.push(newWord);
        }
        output_div.html(output.join(' '));

        var words = Object.keys(counter);
        var wordCount = words.length;

        if (wordCount) {
            var output = '<ul>';
            for (word of words) {
                var size = counter[word];
                output += '<li style="font-size: ' + size + '0pt">' + word + ': ' + size + '</li>';
            }
            output += '</ul>'
            $('#wordcount').html(wordCount);
        } else {
            var output = '<h3>Поздаврляю! У вас чистейший Русский!🇷🇺</h3>';
        }

        stats_div.html(output);

        $('html, body').animate({
            scrollTop: parseInt($('#resultdiv').offset().top)
        }, 900);
    });
});