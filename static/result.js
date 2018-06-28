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
var palette = "";
function set_palette(colors) {
    palette = colors
}

function set_prompt_color(palette) {
    prompt = "[[b;{4};]root][[b;{1};]@][[b;{2};]pywal]\n [[;{1};]❯][[;{3};]❯][[;{2};]❯] ".format(
        palette["0"],
        palette["1"],
        palette["2"],
        palette["3"],
        palette["4"]
    );
    $('#terminal').terminal().set_prompt(prompt);
}

function help(term) {
    term.echo("Available commands:\n\thelp\tls\twhoami");
}

function incorrect_command(term) {
    var insults=[
        "Boooo!",
        "Don't you know anything?",
        "RTFM!",
        "Hahaha, n00b!",
        "Wow! That was impressively wrong!",
        "What are you doing??",
        "Pathetic",
        "...and this is the best you can do??",
        "The worst one today!",
        "n00b alert!",
        "Your application for reduced salary has been sent!",
        "lol",
        "u suk",
        "lol... plz",
        "plz uninstall",
        "And the Darwin Award goes to.... ",
        "ERROR_INCOMPETENT_USER",
        "Incompetence is also competence",
        "Bad.",
        "Fake it till you make it!",
        "What is this...? Amateur hour!?",
        "Come on! You can do it!",
        "Nice try.",
        "What if... you type an actual command the next time!",
        "What if I told you... it is possible to type valid commands.",
        "Y u no speak computer???",
        "This is not Windows",
        "Perhaps you should leave the command line alone...",
        "Please step away from the keyboard!",
        "error code: 1D10T",
        "Pro tip: type a valid command!",
    ];

    var insult = insults[Math.floor(Math.random() * insults.length)];
    term.echo(insult);
    help(term);
}

function interpreter(input, term) {
    var command, inputs;
    inputs = input.split(/ +/)
    command = inputs[0];
    if (command === "ls") {
        term.echo(
            "[[;{4};]Dir] [[;{2};]executable.sh] [[;{5};]file.jpg] [[;{6};]symlink] [[;{7};].bash_profile]".format(
                palette["0"],
                palette["1"],
                palette["2"],
                palette["3"],
                palette["4"],
                palette["5"],
                palette["6"],
                palette["7"],

            )
        );
    } else if (command === "help") {
        help(term);
    } else if (/whoami/.test(input)) {
        term.echo("root");
    } else if (command.length === 0) {
    } else {
        incorrect_command(term);
    }
}

$('#terminal').terminal(interpreter, {
    prompt: prompt,
    greetings: false,
    height: 600,
    onInit: function (term) {
        term.history().clear();
    }
});


