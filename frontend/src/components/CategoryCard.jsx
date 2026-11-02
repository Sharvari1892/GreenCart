import { Link } from "react-router-dom";

/** Maps category name keywords to an emoji icon */
function getCategoryEmoji(name = "") {
  const n = name.toLowerCase();
  if (n.includes("produce") || n.includes("fruit") || n.includes("vegetable") || n.includes("fresh"))
    return "🥦";
  if (n.includes("dairy") || n.includes("milk") || n.includes("cheese") || n.includes("egg"))
    return "🥛";
  if (n.includes("meat") || n.includes("poultry") || n.includes("fish") || n.includes("seafood"))
    return "🥩";
  if (n.includes("bakery") || n.includes("bread") || n.includes("grain") || n.includes("cereal"))
    return "🍞";
  if (n.includes("beverage") || n.includes("drink") || n.includes("juice") || n.includes("water"))
    return "🧃";
  if (n.includes("snack") || n.includes("chip") || n.includes("candy") || n.includes("sweet"))
    return "🍪";
  if (n.includes("frozen"))
    return "🧊";
  if (n.includes("personal") || n.includes("care") || n.includes("hygiene") || n.includes("beauty"))
    return "🧴";
  if (n.includes("kitchen") || n.includes("home") || n.includes("house"))
    return "🍽️";
  if (n.includes("cloth") || n.includes("apparel") || n.includes("fashion"))
    return "👕";
  if (n.includes("electronics") || n.includes("tech") || n.includes("gadget"))
    return "💡";
  if (n.includes("essential") || n.includes("everyday"))
    return "🛍️";
  if (n.includes("clean") || n.includes("detergent"))
    return "🧼";
  if (n.includes("organic"))
    return "🌿";
  return "🛒";
}

/**
 * CategoryCard — displays a single category tile.
 * Props:
 *   category   { id, name, description } — category object from API
 *   onSelect   (categoryId) => void       — called on click (optional)
 */
function CategoryCard({ category, onSelect }) {
  const emoji = getCategoryEmoji(category.name);

  const handleClick = (e) => {
    if (onSelect) {
      e.preventDefault();
      onSelect(category.id);
    }
  };

  return (
    <Link
      to="/products"
      className="category-card"
      onClick={handleClick}
      aria-label={`Browse ${category.name}`}
    >
      <div className="category-icon" aria-hidden="true">
        {emoji}
      </div>
      <span className="category-name">{category.name}</span>
      {category.description && (
        <span className="category-desc">{category.description}</span>
      )}
    </Link>
  );
}

export default CategoryCard;
