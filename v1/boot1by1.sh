SRC="bl-comp1.bl1"
VM="blSECD.py"
BIN0="bl-comp1.blSECD0"
BIN1="bl-comp1.blSECD1"
S0="out-1by1-0"
S1="out-1by1-1"
S2="out-1by1-2"

python3 "$VM" "$BIN0" < "$SRC" > "$S0" && \
python3 "$VM" "$S0" < "$SRC" > "$S1" && \
python3 "$VM" "$S1" < "$SRC" > "$S2" && \
diff -u "$S0" "$S1" && \
diff -u "$S1" "$S2" && \
diff -u "$S2" "$S0" && \
cp -p "$S2" "$BIN1" && \
rm "$S0" "$S1" "$S2"

