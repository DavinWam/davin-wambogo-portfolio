// stylelint.config.js
module.exports = {
  extends: ["stylelint-config-standard"],
  plugins: ["stylelint-order"],
  rules: {
    // Force alphabetical ordering of properties
    "order/properties-alphabetical-order": true,
  },
};
