function pootpoot () {
var ADJ_V = ['honest', 'insane', 'emotional', 'empty', 'absent-minded', 'aloof', 'impossible', 'open-minded', 'original', 'underated', 'ugly', 'unequalled'];
var ADJ_C = ['friendly', 'happy', 'true', 'perfect', 'wild', 'lousy', 'foolish', 'stinky', 'radiant', 'weak', 'half-hearted', 'passionate'];
var NOUN_M = ['man', 'boy'];
var NOUN_F = ['woman', 'lady', 'girl'];
var NOUN_U = ['world', 'friend', 'home', 'lie', 'love', 'feeling', 'reaction', 'dollar', 'car', 'ship'];
var PREDICATES = ['is always', 'is never', 'can be', 'cannot be', 'will always seem', 'may never seem', 'is worth', 'is greater than', 'can never be'];

function wpoot_subject () {
    var chunk = r(0, 1) ? 'an ' + ADJ_V[r(0, ADJ_V.length - 1)] : 'a ' + ADJ_C[r(0, ADJ_C.length - 1)];
    chunk = r(0, 3)
        ? chunk + ' '
        : 'a ';

    var choice = r(0, 5);

    if (choice < 2) {
        chunk += NOUN_F[r(0, NOUN_F.length - 1)];
    } else if (choice > 2) {
        chunk += NOUN_U[r(0, NOUN_U.length - 1)];
    } else {
        chunk += NOUN_M[r(0, NOUN_M.length - 1)];
    }

    return chunk;
}

function wpoot_object () {
    var chunk = r(0, 1)
        ? ADJ_V[r(0, ADJ_V.length - 1)]
        : ADJ_C[r(0, ADJ_C.length - 1)];
    chunk = r(0, 1)
        ? chunk
        : wpoot_subject();
    return chunk;
}

function wpoot_predicate () {
    return PREDICATES[r(0, PREDICATES.length - 1)];
}

return {
    'start': function (target) { 
        var wpoot = function (target) {
            target.unbind('click');
            target.click(function () { wpoot(target); });
            target.text(wpoot_subject() + " " + wpoot_predicate() + " " + wpoot_object() + ".");
            target.wrapInner('<h1></h1>');
        };
        wpoot(target);
    },
    'stop': function () { }
};
}
