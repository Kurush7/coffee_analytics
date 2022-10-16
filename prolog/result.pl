% итоговый результат по способу приготовления
результат([], Modifiers, Res):- объединение_модификаторов(Modifiers, Res).
результат([H|Stuff], Modifiers, Res):-
    модификатор_или_пустой(H, M),
    Modifiers1 = [M|Modifiers],
    результат(Stuff, Modifiers1, Res).

результат(Method, Res):-
    Method = способ_приготовления(Name, Ingredients, Instruments),
    smart_append(Ingredients, Instruments, Stuff),
    модификатор_или_пустой(Method, M),
    результат(Stuff, [M], Res).

% если в ингредиентах не только кофе - они перебивают все потенциальные оценки
smart_append([X], Instruments, Stuff):- X = ингредиент(кофе, _,_,_,_), append([X], Instruments, Stuff), !.
smart_append(Ingredients, Instruments, Stuff):-
    exclude_coffee(Ingredients, Stuff).


exclude_coffee([], Tmp, Tmp).
exclude_coffee([ингредиент(кофе, _,_,_,_)|T], Tmp, Res):- exclude_coffee(T, Tmp, Res), !.
exclude_coffee([H|T], Tmp, Res):- exclude_coffee(T, [H|Tmp], Res).
exclude_coffee(Ingredients, Res):- exclude_coffee(Ingredients, [], Res).