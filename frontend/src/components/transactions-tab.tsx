'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { History, ArrowUpCircle, ArrowDownCircle, X, AlertTriangle } from 'lucide-react'
import { formatCurrency, formatDate } from '@/lib/utils'
import { useToast } from '@/components/ui/use-toast'
import apiService from '@/services/api'
import type { Transaction, Subscription } from '@/types'

interface TransactionsTabProps {
  transactions: Transaction[]
  subscriptions: Subscription[]
  onUpdate: () => void
}

export function TransactionsTab({ transactions, subscriptions, onUpdate }: TransactionsTabProps) {
  const [filter, setFilter] = useState<'all' | 'subscription' | 'cancellation'>('all')
  const [selectedSubscription, setSelectedSubscription] = useState<Subscription | null>(null)
  const [isCancelling, setIsCancelling] = useState(false)
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const { toast } = useToast()

  const filteredTransactions = transactions.filter(transaction => {
    if (filter === 'all') return true
    return transaction.transaction_type === filter
  })

  const activeSubscriptions = subscriptions.filter(s => s.is_active)

  const handleCancelSubscription = async () => {
    if (!selectedSubscription) return

    setIsCancelling(true)
    try {
      await apiService.subscriptions.cancel({
        subscription_id: selectedSubscription.id,
      })

      toast({
        title: "¡Cancelación exitosa!",
        description: `Has cancelado la suscripción a ${selectedSubscription.fund_name}`,
      })

      setIsDialogOpen(false)
      onUpdate()
    } catch (error: any) {
      console.error('Error cancelling subscription:', error)
      toast({
        title: "Error en la cancelación",
        description: error.response?.data?.detail || "No se pudo cancelar la suscripción",
        variant: "destructive",
      })
    } finally {
      setIsCancelling(false)
    }
  }

  const getTransactionIcon = (type: string) => {
    switch (type) {
      case 'subscription':
        return <ArrowUpCircle className="h-4 w-4 text-green-600" />
      case 'cancellation':
        return <ArrowDownCircle className="h-4 w-4 text-red-600" />
      default:
        return <History className="h-4 w-4" />
    }
  }

  const getTransactionColor = (type: string) => {
    switch (type) {
      case 'subscription':
        return 'text-green-600'
      case 'cancellation':
        return 'text-red-600'
      default:
        return 'text-gray-600'
    }
  }

  return (
    <div className="space-y-6">
      {/* Active Subscriptions for Cancellation */}
      {activeSubscriptions.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold mb-4">Cancelar Suscripciones</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {activeSubscriptions.map((subscription) => (
              <Card key={subscription.id}>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-base">{subscription.fund_name}</CardTitle>
                    <Badge variant={subscription.fund_category === 'FPV' ? 'default' : 'secondary'}>
                      {subscription.fund_category}
                    </Badge>
                  </div>
                  <CardDescription>
                    Invertido: {formatCurrency(subscription.amount)}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <div className="text-sm text-muted-foreground">
                      Suscrito el {new Date(subscription.subscribed_at).toLocaleDateString('es-CO')}
                    </div>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => {
                        setSelectedSubscription(subscription)
                        setIsDialogOpen(true)
                      }}
                    >
                      <X className="h-4 w-4 mr-2" />
                      Cancelar
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Transaction History */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Historial de Transacciones</h3>
          <Select value={filter} onValueChange={(value: any) => setFilter(value)}>
            <SelectTrigger className="w-[200px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todas las transacciones</SelectItem>
              <SelectItem value="subscription">Solo suscripciones</SelectItem>
              <SelectItem value="cancellation">Solo cancelaciones</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {filteredTransactions.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-8">
              <History className="h-12 w-12 text-muted-foreground mb-4" />
              <p className="text-lg font-medium text-muted-foreground mb-2">
                No hay transacciones
              </p>
              <p className="text-sm text-muted-foreground text-center">
                {filter === 'all' 
                  ? 'Aún no has realizado ninguna transacción.'
                  : `No hay transacciones de tipo ${filter === 'subscription' ? 'suscripción' : 'cancelación'}.`
                }
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-3">
            {filteredTransactions.map((transaction) => (
              <Card key={transaction.id}>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {getTransactionIcon(transaction.transaction_type)}
                      <div>
                        <p className="font-medium">
                          {transaction.fund_name}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          {transaction.description}
                        </p>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <p className={`font-semibold ${getTransactionColor(transaction.transaction_type)}`}>
                        {transaction.transaction_type === 'subscription' ? '-' : '+'}
                        {formatCurrency(transaction.amount)}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {formatDate(transaction.created_at)}
                      </p>
                    </div>
                  </div>
                  
                  <div className="mt-3 flex items-center justify-between">
                    <Badge variant="outline" className="text-xs">
                      ID: {transaction.transaction_id.slice(0, 8)}...
                    </Badge>
                    <Badge 
                      variant={transaction.status === 'completed' ? 'default' : 'secondary'}
                      className="text-xs"
                    >
                      {transaction.status}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Cancellation Confirmation Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-orange-500" />
              Cancelar Suscripción
            </DialogTitle>
            <DialogDescription>
              ¿Estás seguro de que deseas cancelar tu suscripción a {selectedSubscription?.fund_name}?
            </DialogDescription>
          </DialogHeader>
          
          <div className="py-4">
            <div className="bg-orange-50 border border-orange-200 rounded-md p-4">
              <div className="flex items-start gap-3">
                <AlertTriangle className="h-5 w-5 text-orange-500 mt-0.5" />
                <div>
                  <h4 className="font-medium text-orange-800">Información importante</h4>
                  <ul className="mt-2 text-sm text-orange-700 space-y-1">
                    <li>• Se devolverá el monto completo: {formatCurrency(selectedSubscription?.amount || 0)}</li>
                    <li>• La cancelación es inmediata y no se puede revertir</li>
                    <li>• Recibirás una notificación de confirmación</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
              Mantener Suscripción
            </Button>
            <Button 
              variant="destructive"
              onClick={handleCancelSubscription}
              disabled={isCancelling}
            >
              {isCancelling ? 'Cancelando...' : 'Confirmar Cancelación'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}