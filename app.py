"""
StructNova Africa - Structural Engineering Web Application
Author: Aliyu Bashir Nasir
A Flask web application for structural engineering calculations and portfolio.
"""

import os
import math
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'structnova-africa-secret-key-2026')

# Owner Information
OWNER = {
    'name': 'Aliyu Bashir Nasir',
    'title': 'Future Structural Engineer & Engineering Software Developer',
    'location': 'Nigeria',
    'email': 'aliyu.bashir@structnova.africa',
    'linkedin': 'https://linkedin.com/in/aliyubashirnasir',
    'year': '2026'
}

# Concrete properties (BS 8110 / Eurocode 2 aligned)
CONCRETE_GRADES = {
    'C20': {'fck': 20, 'fctm': 2.2},
    'C25': {'fck': 25, 'fctm': 2.6},
    'C30': {'fck': 30, 'fctm': 2.9},
    'C35': {'fck': 35, 'fctm': 3.2},
    'C40': {'fck': 40, 'fctm': 3.5}
}

# Steel properties
STEEL_GRADES = {
    '460': {'fy': 460, 'Es': 200000},
    '500': {'fy': 500, 'Es': 200000}
}

# Reinforcement bar areas (mm²)
BAR_AREAS = {
    'Y8': 50.3,
    'Y10': 78.5,
    'Y12': 113.1,
    'Y16': 201.1,
    'Y20': 314.2,
    'Y25': 490.9
}


def calculate_slab_design(span, dead_load, live_load, concrete_grade, steel_grade, cover):
    """
    Calculate one-way slab design according to BS 8110 principles.
    
    Returns a dictionary with all calculation steps and results.
    """
    results = {}
    
    # Input parameters
    results['span'] = span
    results['dead_load'] = dead_load
    results['live_load'] = live_load
    results['concrete_grade'] = concrete_grade
    results['steel_grade'] = steel_grade
    results['cover'] = cover
    
    # Material properties
    fck = CONCRETE_GRADES[concrete_grade]['fck']
    fy = STEEL_GRADES[steel_grade]['fy']
    results['fck'] = fck
    results['fy'] = fy
    
    # Step 1: Load Combination (BS 8110: 1.4G + 1.6Q)
    results['load_factor_dead'] = 1.4
    results['load_factor_live'] = 1.6
    ultimate_load = (1.4 * dead_load) + (1.6 * live_load)
    results['ultimate_load'] = round(ultimate_load, 2)
    
    # Step 2: Maximum Bending Moment (simply supported: wL²/8)
    # Convert span to meters for calculation
    moment = (ultimate_load * span ** 2) / 8
    results['moment'] = round(moment, 2)
    results['moment_knm'] = round(moment, 2)
    
    # Step 3: Estimate slab thickness (span/20 to span/28 for slabs)
    # Using span/25 as reasonable estimate
    estimated_depth = (span * 1000) / 25
    # Round to nearest 25mm
    slab_depth = math.ceil(estimated_depth / 25) * 25
    results['slab_depth'] = int(slab_depth)
    
    # Step 4: Effective depth
    # Assume bar diameter of 12mm for initial calculation
    assumed_bar_dia = 12
    effective_depth = slab_depth - cover - (assumed_bar_dia / 2)
    results['effective_depth'] = int(effective_depth)
    results['assumed_bar_dia'] = assumed_bar_dia
    
    # Step 5: Calculate K value (BS 8110)
    # K = M / (bd²fck) where b = 1000mm for slab per meter width
    b = 1000  # mm
    d = effective_depth
    K = (moment * 1e6) / (b * d ** 2 * fck)
    results['K'] = round(K, 4)
    
    # Step 6: Check K against K' (0.156 for BS 8110)
    K_prime = 0.156
    results['K_prime'] = K_prime
    results['compression_reinforcement_needed'] = K > K_prime
    
    # Step 7: Calculate lever arm (z)
    # z = d[0.5 + √(0.25 - K/1.134)] ≤ 0.95d
    if K <= K_prime:
        z = d * (0.5 + math.sqrt(0.25 - K / 1.134))
        z = min(z, 0.95 * d)
    else:
        z = 0.95 * d  # Simplified for K > K'
    results['lever_arm'] = round(z, 1)
    
    # Step 8: Calculate required steel area (As)
    # As = M / (0.87 * fy * z)
    As_required = (moment * 1e6) / (0.87 * fy * z)
    results['As_required'] = round(As_required, 1)
    
    # Step 9: Minimum reinforcement check (BS 8110)
    # As_min = 0.0013 * b * h for fy = 460 MPa
    # As_min = 0.0013 * b * h for fy = 500 MPa (BS 8110-1:1997)
    As_min = 0.0013 * b * slab_depth
    results['As_min'] = round(As_min, 1)
    
    # Use maximum of required and minimum
    As_provided = max(As_required, As_min)
    results['As_provided'] = round(As_provided, 1)
    
    # Step 10: Select reinforcement
    # Try different bar sizes and spacings
    reinforcement_options = []
    
    for bar_size, bar_area in BAR_AREAS.items():
        # Calculate spacing required
        if As_provided > 0:
            spacing = (bar_area * 1000) / As_provided
            # Round down to practical spacing (multiples of 25mm)
            spacing_practical = math.floor(spacing / 25) * 25
            spacing_practical = max(75, min(spacing_practical, 300))  # Limit 75-300mm
            
            As_actual = (bar_area * 1000) / spacing_practical
            
            reinforcement_options.append({
                'bar_size': bar_size,
                'bar_area': bar_area,
                'spacing': spacing_practical,
                'As_actual': round(As_actual, 1),
                'adequate': As_actual >= As_required
            })
    
    # Select best option (adequate with smallest bar, or largest if none adequate)
    adequate_options = [opt for opt in reinforcement_options if opt['adequate']]
    if adequate_options:
        selected = min(adequate_options, key=lambda x: x['bar_area'])
    else:
        selected = max(reinforcement_options, key=lambda x: x['As_actual'])
    
    results['reinforcement_options'] = reinforcement_options
    results['selected_reinforcement'] = selected
    results['reinforcement_suggestion'] = f"{selected['bar_size']} @ {selected['spacing']}mm c/c"
    
    # Step 11: Deflection check (simplified)
    # Basic span/depth ratio for continuous slab = 26
    basic_ratio = 26
    # Modification factor based on tension reinforcement
    if As_provided > 0 and As_required > 0:
        fs = (2 * fy * As_required) / (3 * As_provided)
        # Simplified modification factor
        mf = min(2.0, 0.55 + (477 - fs) / (120 * (0.9 + (moment * 1e6) / (b * d ** 2))))
        mf = max(0.9, mf)
    else:
        mf = 1.0
    
    allowable_span_depth = basic_ratio * mf
    actual_span_depth = (span * 1000) / slab_depth
    
    results['basic_span_depth_ratio'] = basic_ratio
    results['modification_factor'] = round(mf, 2)
    results['allowable_span_depth'] = round(allowable_span_depth, 1)
    results['actual_span_depth'] = round(actual_span_depth, 1)
    results['deflection_ok'] = actual_span_depth <= allowable_span_depth
    
    # Step 12: Shear check (simplified)
    # Design shear force at support
    V = (ultimate_load * span) / 2
    results['shear_force'] = round(V, 2)
    
    # Concrete shear strength (simplified from BS 8110 Table 3.8)
    # vc = 0.79 * (100As/bd)^(1/3) * (400/d)^(1/4) / 1.25
    if As_provided > 0:
        rho = (100 * As_provided) / (b * d)
        vc = 0.79 * (rho ** (1/3)) * ((400/d) ** (1/4)) / 1.25
        vc = min(vc, 0.8 * math.sqrt(fck))  # Limit to 0.8√fck
    else:
        vc = 0.4
    
    results['concrete_shear_strength'] = round(vc, 2)
    results['shear_ok'] = (V * 1000) / (b * d) <= vc
    
    return results


@app.route('/')
def index():
    """Home page route."""
    return render_template('index.html', owner=OWNER)


@app.route('/about')
def about():
    """About page route."""
    return render_template('about.html', owner=OWNER)


@app.route('/vision')
def vision():
    """Vision page route."""
    return render_template('vision.html', owner=OWNER)


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    """Structural calculator page route."""
    results = None
    
    if request.method == 'POST':
        try:
            # Get form data
            span = float(request.form.get('span', 0))
            dead_load = float(request.form.get('dead_load', 0))
            live_load = float(request.form.get('live_load', 0))
            concrete_grade = request.form.get('concrete_grade', 'C25')
            steel_grade = request.form.get('steel_grade', '460')
            cover = float(request.form.get('cover', 25))
            
            # Validation
            errors = []
            if span <= 0 or span > 12:
                errors.append("Span must be between 0.1m and 12m")
            if dead_load < 0 or dead_load > 50:
                errors.append("Dead load must be between 0 and 50 kN/m²")
            if live_load < 0 or live_load > 20:
                errors.append("Live load must be between 0 and 20 kN/m²")
            if cover < 15 or cover > 75:
                errors.append("Cover must be between 15mm and 75mm")
            
            if errors:
                for error in errors:
                    flash(error, 'error')
            else:
                results = calculate_slab_design(
                    span, dead_load, live_load,
                    concrete_grade, steel_grade, cover
                )
                flash('Calculation completed successfully!', 'success')
                
        except ValueError:
            flash('Please enter valid numeric values', 'error')
        except Exception as e:
            flash(f'Calculation error: {str(e)}', 'error')
    
    return render_template(
        'calculator.html',
        owner=OWNER,
        concrete_grades=list(CONCRETE_GRADES.keys()),
        steel_grades=list(STEEL_GRADES.keys()),
        results=results
    )


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('index.html', owner=OWNER), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('index.html', owner=OWNER), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
