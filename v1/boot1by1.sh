SRC="bl-comp1.bl1"
VM="blSECD.py"
BLUTILS="blutils.py"
BLUTILS10="blutils1-0.py"
BLUTILS1="blutils1-0.py"
BIN="bl-comp1.blSECD1"
S0="out-1by1-0"
S1="out-1by1-1"
S2="out-1by1-2"

ln -s "$BLUTILS10" "$BLUTILS" && \
python3 "$VM" "$BIN" < "$SRC" > "$S0" && \
rm "$BLUTILS" && \
ln -s "$BLUTILS1" "$BLUTILS" && \
python3 "$VM" "$S0" < "$SRC" > "$S1" && \
python3 "$VM" "$S1" < "$SRC" > "$S2" && \
diff -u "$S0" "$S1" && \
diff -u "$S1" "$S2" && \
diff -u "$S2" "$S0" && \
cp -p "$S2" "$BIN" && \
rm "$S0" "$S1" "$S2" "$BLUTILS"

