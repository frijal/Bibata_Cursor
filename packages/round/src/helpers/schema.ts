import fs from "fs";
import path from "path";

import { staticCursors, animatedCursors, animatedClip } from "../cursors.json";
import { schemesPath } from "../color";
import { ColorSchema, Configs } from "../types";

// --------------------------------------- Generate Configs 🛠

const generateConfigs = (
  colorSchemes: ColorSchema,
  dirPrefix: string,
  rawSvgsDir: string
) => {
  if (!fs.existsSync(rawSvgsDir)) {
    console.error("🚨🚨 Raw files not Found 🚨🚨");
    process.exit(1);
  }

  const configs: Configs = {};

  for (let [schema] of Object.entries(colorSchemes)) {
    const { base, outline, watch } = colorSchemes[schema];
    const schemaName = `${dirPrefix}-${schema}`;

    const schemaSvgsPath = path.resolve(schemesPath, schemaName);
    fs.mkdirSync(schemaSvgsPath, { recursive: true });

    staticCursors.map((cursor: string) => {
      // Read file
      let content = fs
        .readFileSync(path.resolve(rawSvgsDir, cursor), "utf-8")
        .toString();

      content = content.replace("#00FF00", base).replace("#0000FF", outline);

      // Save Schema
      const cursorPath = path.resolve(schemaSvgsPath, cursor);
      fs.writeFileSync(cursorPath, content, "utf-8");
    });

    for (let [cursor] of Object.entries(animatedCursors)) {
      // Read file
      let content = fs
        .readFileSync(path.resolve(rawSvgsDir, cursor), "utf-8")
        .toString();

      // Animated Cursors have two parts:
      // 1) Cursor Color
      // 2) Watch Color

      content = content.replace("#00FF00", base).replace("#0000FF", outline);

      // try => replace `customize` colors
      // onError => replace `schema` main colors
      try {
        if (!watch) throw new Error("");
        const {
          background: b,
          color1: c1,
          color2: c2,
          color3: c3,
          color4: c4
        } = watch;
        content = content.replace("#TODO", b); // Watch Background
        content = content
          .replace("#TODO", c1)
          .replace("#TODO", c2)
          .replace("#TODO", c3)
          .replace("#TODO", c4);
      } catch (error) {}

      // Save Schema
      const cursorPath = path.resolve(schemaSvgsPath, cursor);
      fs.writeFileSync(cursorPath, content, "utf-8");
    }

    // Creating Dir for store bitmaps
    const bitmapsDir = path.resolve(process.cwd(), "bitmaps", schemaName);
    fs.mkdirSync(bitmapsDir, { recursive: true });

    // push config to Object
    configs[schema] = {
      svgsDir: schemaSvgsPath,
      bitmapsDir,
      animatedCursors,
      staticCursors,
      animatedClip
    };
  }

  return configs;
};

export { generateConfigs };
