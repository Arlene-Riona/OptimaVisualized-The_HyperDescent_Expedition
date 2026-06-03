import numpy as np

def simulate_momentum(initial_x, initial_y, gradient_func, steps=30, lr=0.01, beta=0.9):
    """
    Computes a trajectory path using Gradient Descent with Momentum.
    Formula:
        v_t = beta * v_{t-1} + lr * grad(w_t)
        w_{t+1} = w_t - v_t
    Perfect for building kinetic inertia to glide through flat valley floors.
    """
    path = [[initial_x, initial_y]]
    
    # Initialize velocity vectors for both parameters to zero
    v_x, v_y = 0.0, 0.0
    
    x, y = initial_x, initial_y
    
    for _ in range(steps):
        # Calculate the localized gradients using numerical approximation or specific landscape equations
        grad_x, grad_y = gradient_func(x, y)
        
        # Compute historical kinetic velocity updates
        v_x = beta * v_x + lr * grad_x
        v_y = beta * v_y + lr * grad_y
        
        # Apply step update to parameters
        x = x - v_x
        y = y - v_y
        
        path.append([x, y])
        
    return np.array(path)

def simulate_adam(initial_x, initial_y, gradient_func, steps=30, lr=0.1, beta1=0.9, beta2=0.999, eps=1e-8):
    """
    Computes a trajectory path using the Adam (Adaptive Moment Estimation) Core.
    Formulas:
        m_t = beta1 * m_{t-1} + (1 - beta1) * grad
        v_t = beta2 * v_{t-1} + (1 - beta2) * grad^2
        m_hat = m_t / (1 - beta1^t),  v_hat = v_t / (1 - beta2^t)
        w_{t+1} = w_t - (lr / (sqrt(v_hat) + eps)) * m_hat
    Adapts learning scales independently for steep cliffs vs flat plateaus.
    """
    path = [[initial_x, initial_y]]
    
    # m = 1st moment vector (mean), v = 2nd moment vector (uncentered variance)
    m_x, m_y = 0.0, 0.0
    v_x, v_y = 0.0, 0.0
    
    x, y = initial_x, initial_y
    
    for t in range(1, steps + 1):
        grad_x, grad_y = gradient_func(x, y)
        
        # 1. Update biased first moment estimate
        m_x = beta1 * m_x + (1 - beta1) * grad_x
        m_y = beta1 * m_y + (1 - beta1) * grad_y
        
        # 2. Update biased second raw moment estimate
        v_x = beta2 * v_x + (1 - beta2) * (grad_x ** 2)
        v_y = beta2 * v_y + (1 - beta2) * (grad_y ** 2)
        
        # 3. Compute bias-corrected first moment estimate
        m_x_hat = m_x / (1 - beta1 ** t)
        m_y_hat = m_y / (1 - beta1 ** t)
        
        # 4. Compute bias-corrected second raw moment estimate
        v_x_hat = v_x / (1 - beta2 ** t)
        v_y_hat = v_y / (1 - beta2 ** t)
        
        # 5. Apply adaptive parameter update sequence
        x = x - (lr / (np.sqrt(v_x_hat) + eps)) * m_x_hat
        y = y - (lr / (np.sqrt(v_y_hat) + eps)) * m_y_hat
        
        path.append([x, y])
        
    return np.array(path)