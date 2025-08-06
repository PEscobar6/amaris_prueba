'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Wallet, TrendingUp, History, Settings } from 'lucide-react'
import { formatCurrency } from '@/lib/utils'
import apiService from '@/services/api'
import type { User, Fund, Subscription, Transaction } from '@/types'
import { FundsTab } from '@/components/funds-tab'
import { TransactionsTab } from '@/components/transactions-tab'
import { SettingsTab } from '@/components/settings-tab'

export default function HomePage() {
  const [user, setUser] = useState<User | null>(null)
  const [balance, setBalance] = useState<any>(null)
  const [funds, setFunds] = useState<Fund[]>([])
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([])
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadInitialData()
  }, [])

  const loadInitialData = async () => {
    try {
      setLoading(true)
      const [userProfile, userBalance, fundsData, subscriptionsData, transactionsData] = await Promise.all([
        apiService.user.getProfile(),
        apiService.user.getBalance(),
        apiService.funds.getAll(),
        apiService.subscriptions.getUserSubscriptions(),
        apiService.transactions.getHistory({ limit: 10 }),
      ])

      setUser(userProfile)
      setBalance(userBalance)
      setFunds(fundsData)
      setSubscriptions(subscriptionsData)
      setTransactions(transactionsData)
    } catch (error) {
      console.error('Error loading data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-lg text-muted-foreground">Cargando datos...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Sistema de Gestión FPV
          </h1>
          <p className="text-lg text-gray-600 mt-2">
            Bienvenido, {user?.name || 'Usuario'}
          </p>
        </div>
        
        {/* Balance Card */}
        <Card className="w-full lg:w-auto lg:min-w-[300px]">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Wallet className="h-4 w-4" />
              Saldo Available
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {formatCurrency(user?.balance || 0)}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Actualizado: {new Date().toLocaleDateString('es-CO')}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Fondos Disponibles
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{funds.length}</div>
            <p className="text-xs text-muted-foreground">
              FPV y FIC disponibles
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Suscripciones Activas
            </CardTitle>
            <Badge variant="default" className="text-xs">
              {subscriptions.filter(s => s.is_active).length}
            </Badge>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(subscriptions.reduce((sum, s) => sum + s.amount, 0))}
            </div>
            <p className="text-xs text-muted-foreground">
              Total invertido
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Últimas Transacciones
            </CardTitle>
            <History className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{transactions.length}</div>
            <p className="text-xs text-muted-foreground">
              Este mes
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs defaultValue="funds" className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="funds">Fondos</TabsTrigger>
          <TabsTrigger value="transactions">Historial</TabsTrigger>
          <TabsTrigger value="settings">Configuración</TabsTrigger>
        </TabsList>
        
        <TabsContent value="funds">
          <FundsTab 
            funds={funds} 
            subscriptions={subscriptions}
            onUpdate={loadInitialData}
          />
        </TabsContent>
        
        <TabsContent value="transactions">
          <TransactionsTab 
            transactions={transactions}
            subscriptions={subscriptions}
            onUpdate={loadInitialData}
          />
        </TabsContent>
        
        <TabsContent value="settings">
          <SettingsTab 
            user={user}
            onUpdate={loadInitialData}
          />
        </TabsContent>
      </Tabs>
    </div>
  )
}