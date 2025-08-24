module.exports = {
  extends: ["stylelint-config-standard"],
  plugins: ["stylelint-order"],
  rules: {
    // Force alphabetical ordering of properties
    "order/properties-alphabetical-order": true,
    "declaration-block-single-line-max-declarations": 1,

    // BEM-friendly class names
    "selector-class-pattern": [
      "^(?:[a-z0-9]+(?:-[a-z0-9]+)*)(?:__(?:[a-z0-9]+(?:-[a-z0-9]+)*))?(?:--(?:[a-z0-9]+(?:-[a-z0-9]+)*))?$",
      {
        message:
          "Use BEM: block, block__element, block--modifier (kebab-case).",
      },
    ],

    "keyframes-name-pattern": null,
    "no-descending-specificity": null,
  },
};
