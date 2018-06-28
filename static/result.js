if (!String.prototype.format) {
    String.prototype.format = function () {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}

var prompt = "->  ";

function set_prompt_color(palette) {
    prompt = "[[b;{0};]root][[b;{1};]@][[b;{2};]pywal]\n [[;{1};]❯][[;{3};]❯][[;{2};]❯] ".format(
        palette["4"],
        palette["1"],
        palette["2"],
        palette["3"],
    );
    $('#terminal').terminal().set_prompt(prompt);
}

$('#terminal').terminal(function (command) {
    if (command == 'test') {
        this.echo("you just typed 'test'");
    } else {
        this.echo('unknown command');
    }
}, {
    prompt: prompt,
    greetings: false,
    height: 600,
    onInit: function (term) {
        term.history().clear();
    }
});


