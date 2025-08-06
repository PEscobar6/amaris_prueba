// Tipos para el sistema FPV

export interface User {
  id: number
  name: string
  email: string
  phone: string
  balance: number
  notification_preference: 'email' | 'sms'
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Fund {
  id: number
  name: string
  minimum_amount: number
  category: 'FPV' | 'FIC'
  description?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Subscription {
  id: number
  user_id: number
  fund_id: number
  amount: number
  is_active: boolean
  subscribed_at: string
  unsubscribed_at?: string
  fund_name?: string
  fund_category?: string
  fund_minimum_amount?: number
}

export interface Transaction {
  id: number
  transaction_id: string
  user_id: number
  fund_id: number
  transaction_type: 'subscription' | 'cancellation'
  amount: number
  status: string
  description?: string
  created_at: string
  fund_name?: string
  fund_category?: string
  user_name?: string
  user_email?: string
}

export interface SubscriptionRequest {
  fund_id: number
  amount: number
  notification_type?: 'email' | 'sms'
}

export interface CancellationRequest {
  subscription_id: number
}

export interface EligibilityCheck {
  eligible: boolean
  message: string
  user_balance: number
  required_amount: number
  fund_minimum: number
}

export interface ApiResponse<T> {
  data?: T
  message?: string
  error?: string
}