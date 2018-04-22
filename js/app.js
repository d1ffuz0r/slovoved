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

function colorRow(counter) {
    if (0 < counter <= 1) {
        return 'table-info';
    } else if (2 < counter <= 5 ) {
        return 'table-warning'
    } else if (counter > 5) {
        return 'table-danger';
    }
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
                newWord = replaceWord(word, alternative[1]);
                if (counter[alternative[0]]) {
                    counter[alternative[0]].counter += 1
                } else {
                    counter[alternative[0]] = {
                        counter: 1,
                        alternative: alternative[1]
                    }
                }
            }
            output.push(newWord);
        }
        output_div.html(output.join(' '));

        var words = Object.keys(counter);
        var wordCount = words.length;
        var output = '';

        if (wordCount) {
            for (word of words) {
                var alternative = counter[word];
                output += '<tr class="' + colorRow(alternative.counter) + '"><td>' + alternative.counter + '</td><td>' + word + '</td><td>' + alternative.alternative + '</td></tr>';
            }
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