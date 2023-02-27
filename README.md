# Name Generator AI

A Simple name generator created using Keras for training text generation with Artificial Intelligence. </br>
It's not open to be used commercially, however, feel free to use it in any educational or personal project.

## How it works?

This generator adds extra characters to your custom string to generate a fictional name. </br>
You can also change the temperature of the names generated. </br>
The higher the value, more accurate and creative is the names(The default and max value is 1.0).

## How it was trained?

The AI was trained with `names.txt`, a simple dataset with 75189 male and female names what was extracted from Kaggle.

## Limitations

The AI is extremely slow(1 minute on average to generate a name, but it can take it longer), due to specific conditions I insert on the function to generate a more accurate name, since the AI tends to generate gibberishs than proper names 90% of the time.

Also, the AI don't generate names that use specials characters like `'`, `-` or `.` due to lack of enough material to generate proerr name with those characters

Also, the AI takes about 30 minutes to be fully trained with 50 epochs. That's why I saved a `model.h5` file to avoid this training. </br>
Caution: Do not remove anything from `names.txt` or the `model.h5` may not work since it works on a specific shape.

## Basic example

```py
from name_generator_ai import generate_name as gn

for i in range(1, 11):
    print(gn("Ken", temperature=round(i / 10, 1)))  # This is to generate names from a temperature range from 0.1 to 1.0
```

This is the result:

```
Kengt      #Temperature 0.1
Kenfx      #Temperature 0.2
Keneor     #Temperature 0.3
Kenenua    #Temperature 0.4
Kenyhi     #Temperature 0.5
Kenim      #Temperature 0.6
Kenrlaeai  #Temperature 0.7
Kenoeon    #Temperature 0.8
Kennki     #Temperature 0.9
Kenaeyii   #Temperature 1.0, can be turned into Kenaeyi'i later
```

Notice that the first names looks gibberish. </br>
And the middle looks like real names. </br>
While last names looks like fictional names from fantasy books or anything similar to this.
