import sympy as sp
import matplotlib.pyplot as plt
import japanize_matplotlib

# Define symbols for WMW test
n_A, n_B, R_A, R_B, U, U_005 = sp.symbols('n_A n_B R_A R_B U U_{0.05}')

# STEP 1 - Sample sizes and sum of ranks as placeholders
step1_eqs = [
    sp.Eq(sp.Symbol('Sample\ size\ of\ group\ A'), n_A),  # Sample size of group A
    sp.Eq(sp.Symbol('Sample\ size\ of\ group\ B'), n_B),  # Sample size of group B
    sp.Eq(sp.Symbol('Sum\ of\ ranks\ for\ group\ A'), R_A),  # Sum of ranks for group A
    sp.Eq(sp.Symbol('Sum\ of\ ranks\ for\ group\ B'), R_B)   # Sum of ranks for group B
]

# STEP 2 - Equations for calculating U values
U_1 = n_A * n_B + sp.Rational(1, 2) * n_A * (n_A + 1) - R_A
U_2 = n_A * n_B + sp.Rational(1, 2) * n_B * (n_B + 1) - R_B
step2_eqs = [
    sp.Eq(U, U_1),  # U1 calculation
    sp.Eq(U, U_2)   # U2 calculation
]

# STEP 3 - Comparison for significance
step3_eq = [sp.LessThan(U, U_005)]  # U test statistic comparison

# Combine all steps for plotting
all_steps = [('Step 1', step1_eqs), ('Step 2', step2_eqs), ('Step 3', step3_eq)]

# Set up the plot
fig, axs = plt.subplots(len(all_steps), 1, figsize=(8, 6))

# Plot each step
for ax, (step_title, eqs) in zip(axs, all_steps):
    # Use the sympy.latex function to convert equations to LaTeX strings
    text = "\n".join(["$" + sp.latex(eq) + "$" for eq in eqs])
    ax.text(0.5, 0.5, text, fontsize=12, ha='center', va='center', transform=ax.transAxes)
    ax.axis('off')

# Adjust the layout
plt.tight_layout()

# Save the image
image_path = 'wmw_test_equations.png'
plt.savefig(image_path, bbox_inches='tight', pad_inches=0, dpi=300)
plt.close()
