#!/usr/bin/env bash
# Generate the 4 "Systems we build" mockup images via mediagen (needs FAL_KEY set in _shared/mediagen/.env).
# Run once after adding your key:  bash gen-images.sh
# Then in index.html, replace each gallery placeholder block with: <img src="img/<file>.jpg" alt="..." loading="lazy" />
set -e
MG="../../_shared/mediagen/mediagen.py"
OUT="img"
STYLE="clean modern dark UI dashboard, graphite and muted blue accent, structural grid, no text labels, product screenshot, high detail, 16:10"

python "$MG" image --ar 16:9 --yes \
  --prompt "restaurant order management screen, order queue with status, $STYLE" \
  --out "$OUT/system-ordering.jpg"

python "$MG" image --ar 16:9 --yes \
  --prompt "inventory stock control dashboard, stock levels and low-stock alerts, $STYLE" \
  --out "$OUT/system-stock.jpg"

python "$MG" image --ar 16:9 --yes \
  --prompt "demand forecasting chart dashboard, line graph projecting next week, $STYLE" \
  --out "$OUT/system-forecast.jpg"

python "$MG" image --ar 16:9 --yes \
  --prompt "workflow automation flow diagram, nodes and connections, triggers and actions, $STYLE" \
  --out "$OUT/system-automation.jpg"

echo "Done. Now swap the 4 .gallery__shot placeholders in index.html for <img> tags pointing at img/system-*.jpg"
