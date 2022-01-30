SRC="bl-comp0.bl0"
INT="btLISP0.py"
VM="blSECD.py"
BIN="bl-comp0.blSECD0"
S0="out-0by0-0"
S1="out-0by0-1"
S2="out-0by0-2"

python3 "$INT" "$SRC" < "$SRC" > "$S0" &&
python3 "$VM" "$S0" < "$SRC" > "$S1" && \
python3 "$VM" "$S1" < "$SRC" > "$S2" && \
diff -u "$S0" "$S1" && \
diff -u "$S1" "$S2" && \
diff -u "$S2" "$S0" && \
cp -p "$S2" "$BIN" && \
rm "$S0" "$S1" "$S2"

