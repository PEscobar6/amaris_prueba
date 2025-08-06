import axios from 'axios'
import type { 
  User, 
  Fund, 
  Subscription, 
  Transaction, 
  SubscriptionRequest, 
  CancellationRequest, 
  EligibilityCheck 
} from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptors para manejo de errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const apiService = {
  // User endpoints
  user: {
    getProfile: (): Promise<User> =>
      api.get('/user/profile').then(res => res.data),
    
    getBalance: () =>
      api.get('/user/balance').then(res => res.data),
    
    updateNotificationPreference: (preference: 'email' | 'sms'): Promise<User> =>
      api.put('/user/notification-preference', { notification_preference: preference }).then(res => res.data),
  },

  // Funds endpoints
  funds: {
    getAll: (): Promise<Fund[]> =>
      api.get('/funds').then(res => res.data),
    
    getById: (id: number): Promise<Fund> =>
      api.get(`/funds/${id}`).then(res => res.data),
    
    checkEligibility: (fundId: number, amount: number): Promise<EligibilityCheck> =>
      api.get(`/funds/${fundId}/eligibility?amount=${amount}`).then(res => res.data),
  },

  // Subscriptions endpoints
  subscriptions: {
    getUserSubscriptions: (): Promise<Subscription[]> =>
      api.get('/user/subscriptions').then(res => res.data),
    
    subscribe: (data: SubscriptionRequest): Promise<Transaction> =>
      api.post('/subscriptions', data).then(res => res.data),
    
    cancel: (data: CancellationRequest): Promise<Transaction> =>
      api.post('/cancellations', data).then(res => res.data),
  },

  // Transactions endpoints
  transactions: {
    getHistory: (params?: {
      limit?: number
      offset?: number
      transaction_type?: 'subscription' | 'cancellation'
    }): Promise<Transaction[]> =>
      api.get('/transactions', { params }).then(res => res.data),
    
    getById: (transactionId: string): Promise<Transaction> =>
      api.get(`/transactions/${transactionId}`).then(res => res.data),
  },
}

export default apiService