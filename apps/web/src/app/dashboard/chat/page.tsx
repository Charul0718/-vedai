'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../../providers';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Send, MessageSquare, Plus, Compass, Sparkles, User } from 'lucide-react';
import Link from 'next/link';

export default function ChatPage() {
  const { token, user } = useAuth();
  const queryClient = useQueryClient();
  const [typedMessage, setTypedMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Mock messages for demo
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Namaste! I am VedAI, your astrological guide. I can help you understand your Vedic birth chart, planetary placements, and cosmic influences. What would you like to explore today?'
    }
  ]);

  const [isTyping, setIsTyping] = useState(false);

  // Scroll to bottom helper
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!typedMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: typedMessage
    };

    setMessages(prev => [...prev, userMessage]);
    setTypedMessage('');
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const responses = [
        "Based on your Vedic chart, your Sun in Pisces in the 15th house indicates a spiritual and compassionate nature. You may find fulfillment through helping others and exploring mystical knowledge.",
        "Your Moon in Pisces suggests deep emotional sensitivity and a strong intuition. The Uttara Bhadrapada nakshatra gives you a disciplined approach to spiritual growth.",
        "With Scorpio as your ascendant, you have a natural ability to transform and regenerate. Your intensity can be channeled into profound personal growth and helping others heal.",
        "Your current Jupiter Mahadasha with Saturn Antardasha is a significant period for spiritual learning and overcoming challenges through discipline and patience."
      ];
      
      const aiResponse = {
        id: Date.now() + 1,
        role: 'assistant',
        content: responses[Math.floor(Math.random() * responses.length)]
      };

      setMessages(prev => [...prev, aiResponse]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-primary/10">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary to-primary-light flex items-center justify-center text-black font-bold">
            {user?.fullName?.charAt(0) || 'V'}
          </div>
          <div>
            <h3 className="font-semibold text-white">VedAI</h3>
            <p className="text-xs text-slate-400">Your Astrological Guide</p>
          </div>
        </div>
        <button className="p-2 rounded-lg hover:bg-surface/50 transition text-slate-400 hover:text-white">
          <Plus className="h-5 w-5" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.map((msg) => {
          const isUser = msg.role === 'user';
          return (
            <div
              key={msg.id}
              className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex items-start space-x-3 max-w-[80%] ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
                {!isUser && (
                  <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center text-primary shrink-0">
                    <Compass className="h-4 w-4" />
                  </div>
                )}
                <div
                  className={`rounded-2xl p-4 text-sm leading-relaxed ${
                    isUser 
                      ? 'bg-primary text-black rounded-br-none' 
                      : 'bg-surface/50 border border-primary/10 text-slate-300 rounded-bl-none'
                  }`}
                >
                  <div className="whitespace-pre-line">{msg.content}</div>
                </div>
              </div>
            </div>
          );
        })}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="flex items-start space-x-3">
              <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center text-primary shrink-0">
                <Compass className="h-4 w-4" />
              </div>
              <div className="bg-surface/50 border border-primary/10 rounded-2xl rounded-bl-none p-4 text-sm flex items-center space-x-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-primary/10">
        <form onSubmit={handleSendMessage} className="flex items-center space-x-3">
          <div className="flex-1 relative">
            <input
              type="text"
              value={typedMessage}
              onChange={(e) => setTypedMessage(e.target.value)}
              placeholder="Ask about your chart, planets, or cosmic influences..."
              className="w-full rounded-xl border border-primary/20 bg-surface/50 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
            />
          </div>
          <button
            type="submit"
            disabled={!typedMessage.trim()}
            className="p-3 bg-primary text-black rounded-xl hover:bg-primary-light transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="h-5 w-5" />
          </button>
        </form>
        <p className="text-xs text-slate-500 text-center mt-2">
          VedAI provides astrological guidance for self-reflection. Not scientific prediction.
        </p>
      </div>
    </div>
  );
}
