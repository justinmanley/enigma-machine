module EnigmaCode where

{-  Implementation using the State Monad
import Control.Monad.State

type RotorState = State Int

rotors = 3

translate :: Int -> Char -> Char
translate n = numberToLetter . (n+) . letterToNumber 

advance :: (Char,Int) -> (Char,Int)
advance (c,n) = (translate n c, n+1)

encodeChar :: RotorState Char -> RotorState Char
encodeChar = mapState advance -}

{-
data RotorState = RotorState Int Char

instance Monad (RotorState Int) where
    return x = RotorState x
-}

--import Control.Monad.State

{-data RotorState s a = RotorState {
    rSet :: Int, char :: Char
} -}

{-data RotorState s a = RotorState {
    rState :: s -> (a,s)
}

instance Monad (RotorState s) where
    ma >>= g = RotorState $ \s -> let
            (a,s1) = rState ma s
            (b,s2) = rState (g a) s1
         in (b,s2)
    return a = RotorState $ \s -> (a,s)

get :: RotorState s s
get = RotorState $ \s -> (s,s)

put :: Int -> RotorState Int ()
put = \(t :: Int) -> RotorState $ \s -> ((),t+1)

type Encoded a = RotorState Int a

translate :: Int -> Char -> Char
translate n = numberToLetter . (n+) . letterToNumber

advance :: (Int,Char) -> (Int,Char)
advance (n,c) = (n+1,translate n c)

xs = []

next :: Encoded Char -> Encoded Char
next a = do
    char <- a
    b <- get
    let x = b:xs
    put b
    return char -}

data RotorState a = RotorState  ([(Rotor,Rotor)],Rotor,Int) a

instance Monad (RotorState ([(Rotor,Rotor)],Rotor,Int)) where


type Rotor = (Char -> Char,Char -> Char)



--translateChar :: Int -> Char -> Char
--translateChar n = numberToLetter . (n+) . letterToNumber

translateChar :: Char -> (Char -> Char) -> Char
translateChar c f = f c

simpleEncode :: Int -> Char -> Char
simpleEncode n = numberToLetter . loopAround . (n+) . letterToNumber

simpleRotors :: ([Rotor],Rotor)
simpleRotors = ([(simpleEncode 1,simpleEncode (25)),(simpleEncode (24), simpleEncode 3),(simpleEncode 11,simpleEncode (15))], (simpleEncode (18),simpleEncode 8))

lift :: Char -> Encoded Char
lift c = RotorState 0 c

encodeChar :: (([Rotor],Rotor),Char) -> (([Rotor],Rotor),Char)
encodeChar ((a,b),c) = ((a,b),compose (map snd a) . (fst b) . compose (map fst a) $ c) 



--Each time encodeChar is run, it needs to change the state so that the rotors are never in the same position.
--encodeString :: ([Rotor],Rotor) -> String -> String
--encodeString =  

---Utilities---


--Takes a list of functions and an argument and evaluates the composition of all of those functions at the argument.  So compose [f1,f2,f3] x is f1 ( f2 ( f3 (x))).
compose :: [(a -> a)] -> a -> a
compose [] x = x
compose (f:fs) x = compose fs (f x)

--This utility ensures that we stay between 1 and 26 when we are dealing with the numeric representation of the alphabet.
loopAround :: Int -> Int
loopAround n 
    | n > 25 = (n `mod` 26) + 1
    | otherwise = n `mod` 26

numberToLetter :: Int -> Char
numberToLetter n = case n of 1 -> 'a'
                             2 -> 'b'
                             3 -> 'c'
                             4 -> 'd'
                             5 -> 'e'
                             6 -> 'f'
                             7 -> 'g'
                             8 -> 'h'
                             9 -> 'i'
                             10 -> 'j'
                             11 -> 'k'
                             12 -> 'l'
                             13 -> 'm'
                             14 -> 'n'
                             15 -> 'o'
                             16 -> 'p'
                             17 -> 'q'
                             18 -> 'r'
                             19 -> 's'
                             20 -> 't'
                             21 -> 'u'
                             22 -> 'v'
                             23 -> 'w'
                             24 -> 'x'
                             25 -> 'y'
                             26 -> 'z'

letterToNumber :: Char -> Int
letterToNumber c = case c of 'a' -> 1
                             'b' -> 2
                             'c' -> 3
                             'd' -> 4
                             'e' -> 5
                             'f' -> 6
                             'g' -> 7
                             'h' -> 8
                             'i' -> 9
                             'j' -> 10
                             'k' -> 11
                             'l' -> 12
                             'm' -> 13
                             'n' -> 14
                             'o' -> 15
                             'p' -> 16
                             'q' -> 17
                             'r' -> 18
                             's' -> 19
                             't' -> 20
                             'u' -> 21
                             'v' -> 22
                             'w' -> 23
                             'x' -> 24
                             'y' -> 25
                             'z' -> 26

